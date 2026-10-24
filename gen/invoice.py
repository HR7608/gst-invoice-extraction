import random
from datetime import date, timedelta

from gstin import STATES, make_gstin

COMPANIES = [
    "Sharma Traders", "Patel Electronics", "Krishna Enterprises",
    "Gupta & Sons", "Reddy Industries", "Singh Hardware",
    "Mehta Textiles", "Iyer Stationers", "Verma Agencies", "Nair Foods",
]

# (description, hsn, gst_rate)
ITEMS = [
    ("LED Bulb 9W", "853950", 12), ("Copper Wire 2.5mm", "854411", 18),
    ("Office Chair", "940130", 18), ("A4 Paper Ream", "480256", 12),
    ("Cotton Fabric", "520812", 5), ("Basmati Rice 25kg", "100630", 5),
    ("Laptop Bag", "420292", 18), ("Steel Bolts M8", "731815", 18),
    ("Water Bottle", "392410", 18), ("Notebook 200pg", "482020", 12),
]


def make_invoice():
    seller_code = random.choice(list(STATES))
    # 60% same state (CGST+SGST), 40% different state (IGST)
    if random.random() < 0.6:
        buyer_code = seller_code
    else:
        buyer_code = random.choice([c for c in STATES if c != seller_code])

    buyer_gstin = make_gstin(buyer_code) if random.random() < 0.8 else None

    items = []
    for desc, hsn, rate in random.sample(ITEMS, random.randint(1, 5)):
        items.append({
            "description": desc,
            "hsn": hsn,
            "quantity": random.randint(1, 50),
            "unit_price": round(random.uniform(20, 5000), 2),
            "gst_rate": rate,
        })

    tax = sum(i["quantity"] * i["unit_price"] * i["gst_rate"] / 100 for i in items)
    taxable = sum(i["quantity"] * i["unit_price"] for i in items)
    intra = seller_code == buyer_code
    cgst = round(tax / 2, 2) if intra else 0.0
    sgst = cgst
    igst = 0.0 if intra else round(tax, 2)
    total = round(taxable + cgst + sgst + igst, 2)

    inv_date = date(2026, 4, 1) + timedelta(days=random.randint(0, 200))
    return {
        "invoice_number": f"INV/{random.randint(2025, 2026)}/{random.randint(1, 9999):04d}",
        "invoice_date": inv_date.isoformat(),
        "seller": {"name": random.choice(COMPANIES),
                   "gstin": make_gstin(seller_code), "state": STATES[seller_code]},
        "buyer": {"name": random.choice(COMPANIES),
                  "gstin": buyer_gstin, "state": STATES[buyer_code]},
        "line_items": items,
        "cgst": cgst, "sgst": sgst, "igst": igst,
        "total_amount": total,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(make_invoice(), indent=2))
