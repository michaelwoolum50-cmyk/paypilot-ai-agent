# 🤖 PayPilot — AI Agentic Commerce

**PayPal AI Hackathon 2026 entry.** Tell PayPilot what you want and your max budget.
Its AI agent searches listings, reasons about the best deal, and checks out with
**PayPal** — or watches prices on autopilot and buys the moment your target hits.

## What it does

- **Shop once** — describe a product + budget → the agent scores every listing
  (price headroom, seller rating, condition, shipping) and picks the winner.
- **PayPal checkout** — the agent creates a real PayPal Orders API v2 order
  (sandbox) and hands you the approval link. No real money moves.
- **Autopilot watch** — set a target price + hard spending cap; the agent
  monitors 30-day price history and executes the purchase when the deal appears.
- **Transparent reasoning trace** — every decision is explained line-by-line in
  the UI, so judges (and buyers) see exactly why the agent chose what it did.

## Quick start

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

Works immediately in **preview mode** (no keys needed) — the full agent loop,
scoring, and trace all run offline.

## Enable live PayPal sandbox orders (5 minutes, free)

1. Go to https://developer.paypal.com → **Log in / Sign up** (free).
2. **Apps & Credentials** → toggle to **Sandbox** → **Create App** → name it `PayPilot`.
3. Copy the **Client ID** and **Secret**.
4. Export them and restart:
   ```bash
   export PAYPAL_CLIENT_ID="your-sandbox-client-id"
   export PAYPAL_CLIENT_SECRET="your-sandbox-secret"
   python app.py
   ```
5. Uncheck "Preview only" in the UI and shop — the agent creates a real
   sandbox order. Approve it with a sandbox buyer account from
   developer.paypal.com → **Sandbox → Accounts** (PayPal provides test buyers).

## Optional: upgrade the AI narration

The agent's scoring engine runs fully offline. To add LLM-generated reasoning
notes, point it at any OpenAI-compatible chat endpoint:

```bash
export PAYPILOT_LLM_URL="https://api.groq.com/openai/v1/chat/completions"
export PAYPILOT_LLM_KEY="your-key"
export PAYPILOT_LLM_MODEL="llama-3.3-70b-versatile"
```

## Swap in live product data

`agent/catalog.py` ships a built-in catalog so judges can run it with zero keys.
`search_products(query, limit)` is the only interface the agent uses — replace
its body with eBay Browse API calls (free app key at developer.ebay.com) and
everything else keeps working.

## Run the tests

```bash
python tests/test_shopper.py
```

## Project layout

```
app.py                 Flask app (UI + JSON API)
agent/
  shopper.py           the agentic loop (search → reason → pay)
  brain.py             deal scoring + explainable reasoning
  catalog.py           product listings (mock; eBay-ready interface)
  paypal_client.py     PayPal Orders API v2 (sandbox), no SDK needed
templates/index.html   UI
static/                CSS + JS
tests/                 agent tests (no network)
```

## Tools used

- **PayPal Developer Platform** — Orders API v2 (sandbox): order creation is the
  heart of the agentic-commerce loop; the agent cannot complete a purchase
  without it.
- **AI** — built-in explainable scoring engine (offline); optional
  OpenAI-compatible LLM for natural-language reasoning notes.

## License

MIT — see LICENSE.
