"""PayPilot — AI agentic commerce. Tell it what you want; it finds the
deal and pays with PayPal. Built for the PayPal AI Hackathon 2026."""
import os
from flask import Flask, render_template, request, jsonify
from agent import shopper

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/shop", methods=["POST"])
def api_shop():
    data = request.get_json(force=True)
    query = (data.get("query") or "").strip()
    try:
        max_budget = float(data.get("max_budget") or 0)
    except ValueError:
        return jsonify({"error": "Budget must be a number."}), 400
    if not query or max_budget <= 0:
        return jsonify({"error": "Give me a product and a max budget."}), 400
    dry = bool(data.get("dry_run"))
    result = shopper.shop_once(query, max_budget, create_paypal_order=not dry)
    return jsonify(result)


@app.route("/api/watch", methods=["POST"])
def api_watch():
    data = request.get_json(force=True)
    query = (data.get("query") or "").strip()
    try:
        target = float(data.get("target_price") or 0)
        cap = float(data.get("max_budget") or 0)
    except ValueError:
        return jsonify({"error": "Prices must be numbers."}), 400
    if not query or target <= 0 or cap <= 0:
        return jsonify({"error": "Need a product, target price and hard cap."}), 400
    return jsonify(shopper.autopilot_watch(query, target, cap))


@app.route("/api/health")
def health():
    return jsonify({"ok": True,
                    "paypal_configured": bool(os.environ.get("PAYPAL_CLIENT_ID"))})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
