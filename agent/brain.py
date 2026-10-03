"""PayPilot brain — scores deals and explains its reasoning.

Two modes:
  heuristic (default): transparent scoring, zero API keys, fully offline.
  llm (optional): set PAYPILOT_LLM_URL to any OpenAI-compatible chat
      completions endpoint and PAYPILOT_LLM_KEY to upgrade the reasoning
      narrative. The heuristic score still gates every purchase.
"""
import json
import os
import urllib.request

CONDITION_PENALTY = {
    "new": 0.0, "open-box": 0.06, "new-damaged-box": 0.08,
    "renewed": 0.10, "refurbished": 0.12, "used": 0.18,
}


def score_listing(listing, max_budget):
    """Return (score 0-100, reasons[]). Higher is better."""
    reasons = []
    price = listing["price"]
    if price > max_budget:
        return 0, ["over budget ($%.2f > $%.2f)" % (price, max_budget)]
    score = 60.0
    # headroom under budget: cheaper relative to budget wins
    headroom = (max_budget - price) / max_budget
    score += headroom * 20
    reasons.append("$%.2f under a $%.2f budget" % (max_budget - price, max_budget))
    # seller rating
    rating = listing.get("seller_rating", 4.0)
    score += (rating - 4.0) * 10
    reasons.append("seller rating %.1f/5" % rating)
    # condition penalty
    pen = CONDITION_PENALTY.get(listing.get("condition", "new"), 0.10)
    score -= pen * 100
    if pen:
        reasons.append("condition '%s' (-%d)" % (listing["condition"], pen * 100))
    # fast shipping bonus
    if listing.get("shipping_days", 7) <= 3:
        score += 5
        reasons.append("fast shipping (%dd)" % listing["shipping_days"])
    return max(0, min(100, round(score, 1))), reasons


def _llm_narrate(prompt):
    url = os.environ.get("PAYPILOT_LLM_URL", "")
    key = os.environ.get("PAYPILOT_LLM_KEY", "")
    if not url or not key:
        return None
    try:
        body = json.dumps({
            "model": os.environ.get("PAYPILOT_LLM_MODEL", "llama-3.3-70b-versatile"),
            "messages": [{"role": "user", "content": prompt[:2000]}],
            "max_tokens": 220, "temperature": 0.4,
        }).encode()
        req = urllib.request.Request(
            url, data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + key})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.load(r)
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


def pick_deal(query, listings, max_budget, prefer_new=True):
    """Choose the best listing. Returns dict with pick + full trace."""
    trace = ["Shopper request: '%s' (max $%.2f)" % (query, max_budget),
             "Found %d candidate listings" % len(listings)]
    scored = []
    for l in listings:
        s, reasons = score_listing(l, max_budget)
        if prefer_new and l.get("condition") not in ("new",):
            s -= 4
            reasons.append("prefer-new bias (-4)")
        scored.append((s, l, reasons))
        trace.append("  - %s: $%.2f -> score %.1f (%s)"
                     % (l["title"][:45], l["price"], s, "; ".join(reasons[:2])))
    scored.sort(key=lambda x: -x[0])
    if not scored or scored[0][0] <= 0:
        trace.append("No listing fits the budget. No purchase.")
        return {"pick": None, "trace": trace, "alternatives": []}

    best, best_listing, best_reasons = scored[0]
    trace.append("WINNER: %s ($%.2f, score %.1f)" % (
        best_listing["title"][:50], best_listing["price"], best))

    narrative = _llm_narrate(
        "You are a shopping agent. In 2 sentences explain why this deal wins: "
        "%s at $%.2f. Reasons: %s. Budget was $%.2f." % (
            best_listing["title"], best_listing["price"],
            "; ".join(best_reasons), max_budget))
    if narrative:
        trace.append("AI note: " + narrative)
    return {"pick": best_listing, "score": best,
            "reasons": best_reasons, "trace": trace,
            "alternatives": [s[1] for s in scored[1:4]]}
