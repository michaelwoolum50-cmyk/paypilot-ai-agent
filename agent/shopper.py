"""PayPilot shopper — the agentic commerce loop.

shop_once(query, max_budget): search -> reason -> (optionally) PayPal order.
autopilot_watch(...): monitor a product; buy when it drops under target.
Every run returns a full reasoning trace for the UI and the demo.
"""
from . import catalog, brain
from .paypal_client import PayPalClient


def shop_once(query, max_budget, create_paypal_order=True,
              prefer_new=True, paypal=None):
    trace = []
    listings = catalog.search_products(query)
    trace.append("PayPilot agent started.")
    if not listings:
        trace.append("No listings matched '%s'." % query)
        return {"status": "no_results", "trace": trace}

    decision = pick = brain.pick_deal(query, listings, max_budget, prefer_new)
    trace.extend(decision["trace"])
    result = {"status": "evaluated", "trace": trace,
              "pick": decision["pick"], "score": decision.get("score"),
              "alternatives": decision.get("alternatives", [])}

    if not decision["pick"]:
        result["status"] = "no_deal"
        return result

    if not create_paypal_order:
        result["status"] = "deal_found"
        trace.append("Dry run: PayPal order NOT created (preview mode).")
        return result

    try:
        pp = paypal or PayPalClient()
        order_id, approval_url = pp.create_order(
            decision["pick"]["price"], "USD",
            "PayPilot: " + decision["pick"]["title"][:100])
        trace.append("PayPal sandbox order created: %s" % order_id)
        trace.append("Buyer approves here: %s" % approval_url)
        result.update({"status": "order_created", "order_id": order_id,
                       "approval_url": approval_url})
    except Exception as e:
        trace.append("PayPal order failed: %s" % str(e)[:160])
        result["status"] = "paypal_error"
        result["error"] = str(e)[:200]
    return result


def autopilot_watch(query, target_price, max_budget, paypal=None):
    """Simulate a price watch: check 30-day history, buy if it ever
    dipped under target within budget. Returns trace + decision."""
    trace = ["Autopilot watch: '%s' (buy under $%.2f, hard cap $%.2f)"
             % (query, target_price, max_budget)]
    listings = catalog.search_products(query, limit=5)
    if not listings:
        return {"status": "no_results", "trace": trace}
    for l in listings:
        hist = catalog.price_history(l["id"])
        low = min(hist)
        trace.append("%s: 30-day low $%.2f (now $%.2f)"
                     % (l["title"][:40], low, l["price"]))
        if low <= target_price and l["price"] <= max_budget:
            trace.append("Target hit on %s — executing purchase." % l["id"])
            return shop_once(l["title"], max_budget,
                             create_paypal_order=True, paypal=paypal)
    trace.append("No listing under target. Still watching.")
    return {"status": "watching", "trace": trace}
