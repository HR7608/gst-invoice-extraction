import random


def money(x):
    style = random.choice(["plain", "rs", "inr"])
    s = f"{x:.2f}"
    if style == "rs":
        return f"Rs. {s}"
    if style == "inr":
        return f"INR {s}"
    return s


def noise(text):
    out = []
    for line in text.split("\n"):
        join = random.random() < 0.08
        if random.random() < 0.1:
            line = line.replace(" ", "  ")
        out.append(line + (" " if join else "\n"))
    return "".join(out).strip()


def layout_a(inv):
    lines = ["TAX INVOICE", f"Invoice No: {inv['invoice_number']}",
             f"Date: {inv['invoice_date']}", "",
             f"Seller: {inv['seller']['name']}",
             f"GSTIN: {inv['seller']['gstin']}",
             f"State: {inv['seller']['state']}", "",
             f"Bill To: {inv['buyer']['name']}"]
    if inv["buyer"]["gstin"]:
        lines.append(f"Buyer GSTIN: {inv['buyer']['gstin']}")
    lines += [f"State: {inv['buyer']['state']}", "", "Items:"]
    for i in inv["line_items"]:
        lines.append(f"{i['description']} | HSN {i['hsn']} | Qty {i['quantity']} "
                     f"| Rate {money(i['unit_price'])} | GST {i['gst_rate']}%")
    lines += ["", f"CGST: {money(inv['cgst'])}", f"SGST: {money(inv['sgst'])}",
              f"IGST: {money(inv['igst'])}", f"Grand Total: {money(inv['total_amount'])}"]
    return "\n".join(lines)


def layout_b(inv):
    lines = ["INVOICE", f"Inv #: {inv['invoice_number']}   Dated: {inv['invoice_date']}", "",
             f"Customer: {inv['buyer']['name']} ({inv['buyer']['state']})"]
    if inv["buyer"]["gstin"]:
        lines.append(f"Customer GST No: {inv['buyer']['gstin']}")
    lines += ["", f"Supplier: {inv['seller']['name']} ({inv['seller']['state']})",
              f"Supplier GST No: {inv['seller']['gstin']}", "",
              "Description    HSN    Qty    Price    Tax%"]
    for i in inv["line_items"]:
        lines.append(f"{i['description']}   {i['hsn']}   {i['quantity']}   "
                     f"{money(i['unit_price'])}   {i['gst_rate']}")
    lines += ["", f"CGST {money(inv['cgst'])}", f"SGST {money(inv['sgst'])}",
              f"IGST {money(inv['igst'])}", f"Total {money(inv['total_amount'])}"]
    return "\n".join(lines)


def render(inv):
    layout = random.choice([layout_a, layout_b])
    return noise(layout(inv))


if __name__ == "__main__":
    from invoice import make_invoice
    inv = make_invoice()
    print(render(inv))
