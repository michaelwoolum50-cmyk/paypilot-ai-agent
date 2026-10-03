"""PayPal Orders API v2 client (sandbox). No SDK dependency — raw REST."""
import base64
import os
import requests

SANDBOX_BASE = "https://api-m.sandbox.paypal.com"


class PayPalClient:
    def __init__(self, client_id=None, client_secret=None, base_url=SANDBOX_BASE):
        self.client_id = client_id or os.environ.get("PAYPAL_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("PAYPAL_CLIENT_SECRET", "")
        self.base_url = base_url
        self._token = None

    def _auth_header(self):
        raw = "%s:%s" % (self.client_id, self.client_secret)
        return "Basic " + base64.b64encode(raw.encode()).decode()

    def get_access_token(self):
        r = requests.post(
            self.base_url + "/v1/oauth2/token",
            headers={"Authorization": self._auth_header(),
                     "Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"},
            timeout=20,
        )
        r.raise_for_status()
        self._token = r.json()["access_token"]
        return self._token

    def _headers(self):
        if not self._token:
            self.get_access_token()
        return {"Authorization": "Bearer " + self._token,
                "Content-Type": "application/json"}

    def create_order(self, amount, currency="USD", description="PayPilot agent purchase"):
        """Create a PayPal order. Returns (order_id, approval_url)."""
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {"currency_code": currency, "value": "%.2f" % amount},
                "description": description[:120],
            }],
            "application_context": {
                "brand_name": "PayPilot",
                "user_action": "PAY_NOW",
            },
        }
        r = requests.post(self.base_url + "/v2/checkout/orders",
                          headers=self._headers(), json=payload, timeout=20)
        r.raise_for_status()
        data = r.json()
        approval = next((l["href"] for l in data.get("links", [])
                         if l.get("rel") == "approve"), "")
        return data["id"], approval

    def capture_order(self, order_id):
        r = requests.post(
            self.base_url + "/v2/checkout/orders/%s/capture" % order_id,
            headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json()

    def get_order(self, order_id):
        r = requests.get(self.base_url + "/v2/checkout/orders/" + order_id,
                         headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json()
