import json
import random

from invoice import make_invoice
from render import noise

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


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


random.seed(11)
rows = []
while len(rows) < 100:
    inv = make_invoice()
    if inv["seller"]["name"] == inv["buyer"]["name"]:
        continue
    rows.append({"text": noise(layout_c(inv)), "label": inv})
with open("../data/test_c.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "rows written")
