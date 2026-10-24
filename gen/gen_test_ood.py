import json
import random

import gstin
import invoice
from render import layout_a, layout_b, noise

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# swap every entity list in place for unseen values
gstin.STATES.clear()
gstin.STATES.update({
    "10": "Bihar", "23": "Madhya Pradesh", "32": "Kerala", "03": "Punjab",
    "21": "Odisha", "18": "Assam", "30": "Goa",
})
invoice.COMPANIES[:] = [
    "Bhatt Agro Mart", "Chopra Cycle Works", "Desai Pharma Distributors",
    "Eswaran Hardware", "Fernandes Traders", "Ghosh Sweets", "Hegde Textiles",
    "Joshi Auto Parts", "Kulkarni Paper Mills", "Lal Dairy Products",
]
invoice.ITEMS[:] = [
    ("Mobile Phone Case", "392690", 18), ("Turmeric Powder 1kg", "091030", 5),
    ("Ceiling Fan", "841451", 18), ("Cement Bag 50kg", "252329", 28),
    ("Handloom Saree", "540752", 5), ("School Bag", "420221", 18),
    ("Tea Leaves 1kg", "090240", 5), ("Air Conditioner 1.5T", "841510", 28),
    ("Printer Cartridge", "844332", 18), ("Fresh Milk Pouch", "040120", 0),
    ("Paddy Seeds 10kg", "100610", 0), ("Tablet Strip Pack", "300490", 12),
]


def layout_c(inv):
    y, m, d = inv["invoice_date"].split("-")
    s, b = inv["seller"], inv["buyer"]
    lines = [f"Bill No. {inv['invoice_number']}   Dt. {d}-{MON[int(m) - 1]}-{y}",
             f"From: {s['name']}, {s['state']} (GSTIN {s['gstin']})"]
    to = f"To: {b['name']}, {b['state']}"
    if b["gstin"]:
        to += f" (GSTIN {b['gstin']})"
    lines += [to, ""]
    for n, i in enumerate(inv["line_items"], 1):
        lines.append(f"{n}) {i['description']} - HSN {i['hsn']} - {i['quantity']} x "
                     f"{i['unit_price']:.2f} @ {i['gst_rate']}% GST")
    lines += ["", f"CGST {inv['cgst']:.2f} | SGST {inv['sgst']:.2f} | IGST {inv['igst']:.2f}",
              f"Amount Payable: {inv['total_amount']:.2f}"]
    return "\n".join(lines)


random.seed(99)
rows = []
while len(rows) < 100:
    inv = invoice.make_invoice()
    if inv["seller"]["name"] == inv["buyer"]["name"]:
        continue
    text = noise(random.choice([layout_a, layout_b, layout_c])(inv))
    rows.append({"text": text, "label": inv})
with open("../data/test_ood.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "rows written")
