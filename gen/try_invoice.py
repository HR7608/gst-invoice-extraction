import sys

import requests

PROMPT = """Extract the invoice below into JSON with exactly this structure:
{"invoice_number": str, "invoice_date": "YYYY-MM-DD",
 "seller": {"name": str, "gstin": str, "state": str},
 "buyer": {"name": str, "gstin": str or null, "state": str},
 "line_items": [{"description": str, "hsn": str, "quantity": number, "unit_price": number, "gst_rate": number}],
 "cgst": number, "sgst": number, "igst": number, "total_amount": number}
Use null for a missing buyer gstin. Output only the JSON.

Invoice:
"""

model, path = sys.argv[1], sys.argv[2]
text = open(path).read()
r = requests.post("http://127.0.0.1:30000/v1/chat/completions", json={
    "model": model, "temperature": 0, "max_tokens": 1500,
    "messages": [{"role": "user", "content": PROMPT + text}]}, timeout=300)
print(r.json()["choices"][0]["message"]["content"])
