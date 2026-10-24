import json

INSTRUCTION = """Extract the invoice below into JSON with exactly this structure:
{"invoice_number": str, "invoice_date": "YYYY-MM-DD",
 "seller": {"name": str, "gstin": str, "state": str},
 "buyer": {"name": str, "gstin": str or null, "state": str},
 "line_items": [{"description": str, "hsn": str, "quantity": number, "unit_price": number, "gst_rate": number}],
 "cgst": number, "sgst": number, "igst": number, "total_amount": number}
Use null for a missing buyer gstin. Output only the JSON."""

n = 0
with open("../data/train_alpaca.jsonl", "w") as out:
    for line in open("../data/train.jsonl"):
        r = json.loads(line)
        out.write(json.dumps({
            "instruction": INSTRUCTION,
            "input": r["text"],
            "output": json.dumps(r["label"], separators=(",", ":"), ensure_ascii=False),
        }, ensure_ascii=False) + "\n")
        n += 1
print(n, "rows written")
