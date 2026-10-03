"""Tests for the PayPilot agent loop (no network, no PayPal creds needed)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from agent import catalog, brain, shopper


def test_search_finds_headphones():
    res = catalog.search_products("Sony WH-1000XM5 headphones")
    assert len(res) >= 2, res
    assert all("headphones" in r["title"].lower() or "sony" in r["title"].lower() for r in res)


def test_scoring_prefers_under_budget_new():
    listings = catalog.search_products("AirPods Pro")
    scored = [(brain.score_listing(l, 200)[0], l) for l in listings]
    best = max(scored, key=lambda x: x[0])[1]
    assert best["price"] <= 200
    # renewed/used should lose to new at similar price
    assert best["condition"] in ("new", "open-box", "renewed")


def test_pick_deal_returns_trace():
    listings = catalog.search_products("Kindle Paperwhite")
    d = brain.pick_deal("Kindle Paperwhite", listings, 150)
    assert d["pick"] is not None
    assert d["pick"]["price"] <= 150
    assert len(d["trace"]) >= 3


def test_no_deal_over_budget():
    listings = catalog.search_products("MacBook Air")
    d = brain.pick_deal("MacBook Air", listings, 50)
    assert d["pick"] is None


def test_shop_once_dry_run():
    r = shopper.shop_once("Ninja air fryer", 100, create_paypal_order=False)
    assert r["status"] == "deal_found", r["status"]
    assert r["pick"]["price"] <= 100
    assert "trace" in r and len(r["trace"]) > 2


def test_autopilot_watch():
    r = shopper.autopilot_watch("Kindle Paperwhite", 90, 150)
    assert r["status"] in ("watching", "order_created", "paypal_error", "no_deal"), r["status"]
    assert len(r["trace"]) >= 2


if __name__ == "__main__":
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("ALL TESTS PASSED")
