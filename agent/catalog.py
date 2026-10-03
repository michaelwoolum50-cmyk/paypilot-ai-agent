"""Mock product catalog — realistic listings the agent shops from.
Swap in the eBay Browse API (see README) for live data; the agent
interface (search_products) is identical."""
import random

_CATALOG = [
    # (title, category, price, seller_rating, shipping_days, condition)
    ("Sony WH-1000XM5 Wireless Noise-Canceling Headphones", "audio", 328.00, 4.8, 3, "new"),
    ("Sony WH-1000XM5 Wireless Noise-Canceling Headphones (Open Box)", "audio", 279.99, 4.6, 5, "open-box"),
    ("Apple AirPods Pro 2nd Gen USB-C", "audio", 189.00, 4.9, 2, "new"),
    ("Apple AirPods Pro 2nd Gen (Renewed)", "audio", 149.50, 4.4, 4, "renewed"),
    ("Bose QuietComfort Ultra Headphones", "audio", 299.00, 4.7, 3, "new"),
    ("Dyson V15 Detect Cordless Vacuum", "home", 549.99, 4.8, 4, "new"),
    ("Dyson V15 Detect (Refurbished)", "home", 419.00, 4.5, 6, "refurbished"),
    ("Shark Stratos Cordless Vacuum", "home", 349.99, 4.6, 3, "new"),
    ("Kindle Paperwhite 16GB", "books", 139.99, 4.9, 2, "new"),
    ("Kindle Paperwhite 16GB (Used - Like New)", "books", 99.00, 4.3, 5, "used"),
    ("LEGO Technic Porsche 911 RSR", "toys", 129.99, 4.9, 3, "new"),
    ("LEGO Technic Porsche 911 RSR (Box Damaged)", "toys", 104.99, 4.2, 7, "new-damaged-box"),
    ("Ninja AF101 Air Fryer 4QT", "kitchen", 89.99, 4.7, 2, "new"),
    ("Ninja AF101 Air Fryer (Certified Refurbished)", "kitchen", 69.99, 4.5, 4, "refurbished"),
    ("Instant Pot Duo 7-in-1 6QT", "kitchen", 79.00, 4.8, 2, "new"),
    ("KitchenAid Artisan Stand Mixer", "kitchen", 379.00, 4.9, 5, "new"),
    ("KitchenAid Artisan Stand Mixer (Refurbished)", "kitchen", 299.99, 4.6, 6, "refurbished"),
    ("Samsung 55\" QLED 4K Smart TV", "tv", 497.99, 4.7, 7, "new"),
    ("LG 55\" OLED evo C4", "tv", 1096.99, 4.9, 7, "new"),
    ("TCL 55\" Q6 QLED 4K TV", "tv", 328.00, 4.5, 4, "new"),
    ("Apple MacBook Air 13\" M3 8GB/256GB", "computers", 899.00, 4.9, 3, "new"),
    ("Apple MacBook Air 13\" M2 (Apple Refurbished)", "computers", 749.00, 4.8, 5, "refurbished"),
    ("Logitech MX Master 3S Mouse", "computers", 79.99, 4.8, 2, "new"),
    ("Dell XPS 13 9340 Laptop", "computers", 999.00, 4.6, 4, "new"),
    ("Herman Miller Aeron Chair (Remastered)", "furniture", 1145.00, 4.9, 10, "new"),
    ("Herman Miller Aeron (Used, Grade A)", "furniture", 549.00, 4.4, 8, "used"),
    ("ErgoChair Pro", "furniture", 299.00, 4.5, 5, "new"),
]


def search_products(query, limit=10):
    """Return listings matching the query, sorted by relevance then price."""
    words = [w.lower() for w in query.split() if len(w) > 2]
    scored = []
    for i, (title, category, price, rating, ship, cond) in enumerate(_CATALOG):
        tl = title.lower()
        hits = sum(1 for w in words if w in tl)
        if not hits and query.lower() not in tl:
            continue
        scored.append((hits, {
            "id": "PP-%04d" % i,
            "title": title,
            "category": category,
            "price": price,
            "seller_rating": rating,
            "shipping_days": ship,
            "condition": cond,
        }))
    scored.sort(key=lambda s: (-s[0], s[1]["price"]))
    return [s[1] for s in scored[:limit]]


def price_history(product_id):
    """Deterministic 30-day price history for the watch/autopilot demo."""
    rng = random.Random(hash(product_id) & 0xFFFFFFFF)
    base = next(p[2] for i, p in enumerate(_CATALOG) if "PP-%04d" % i == product_id)
    return [round(base * (1 + rng.uniform(-0.12, 0.08)), 2) for _ in range(30)]
