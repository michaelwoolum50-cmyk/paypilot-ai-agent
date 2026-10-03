# Devpost Submission — PayPilot (DRAFT for the submission form)

## Tagline
Your AI shopping agent. It finds the deal. PayPal pays.

## Description

**The problem:** Online shopping is a chore — tab-hopping across listings,
comparing prices, second-guessing condition and sellers, then checkout forms.
Nobody has time for that.

**The fix:** PayPilot, an AI agentic-commerce agent. Tell it what you want and
your max budget. The agent searches listings, scores every candidate on price
headroom, seller rating, condition, and shipping speed, explains its reasoning
line-by-line, then creates a real PayPal order so you just approve and own it.

**Autopilot mode** goes further: set a target price and a hard spending cap.
PayPilot watches 30-day price history and executes the purchase the moment your
deal appears — never a cent over your cap.

**Why PayPal is central:** the entire agent loop exists to reach one action —
a PayPal Orders API v2 order. Without PayPal, the agent can recommend; with
PayPal, it can *transact*. That's agentic commerce: AI that doesn't just chat
about buying, but actually buys.

**Why AI matters:** every purchase decision is reasoned, scored, and explained
in a transparent trace — not a black box. An optional LLM upgrade narrates the
decision in natural language.

**Built with:** PayPal Developer Platform (Orders API v2, sandbox), Python/Flask,
built-in explainable AI scoring engine (offline-first; optional OpenAI-compatible
LLM for narration). MIT licensed.

## How it meets the requirements
- Meaningful PayPal integration: order creation/capture via Orders API v2 is the
  agent's core action.
- Meaningful AI: the scoring + reasoning engine drives every purchase decision.
- Working prototype: run locally with zero keys (preview mode) or full PayPal
  sandbox orders with free sandbox creds (5-minute setup, documented in README).
- Public GitHub repo, MIT license, demo video under 3 minutes.
