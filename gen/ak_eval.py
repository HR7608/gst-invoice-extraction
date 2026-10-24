import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import requests

import auditkit as ak

NAME = sys.argv[1]
TEST = sys.argv[2]
N = int(sys.argv[3]) if len(sys.argv) > 3 else 100
URL = "http://127.0.0.1:30000/v1/chat/completions"
OUT = f"../data/pred_{NAME}_{os.path.basename(TEST)}"

PROMPT = """Extract the invoice below into JSON with exactly this structure:
{"invoice_number": str, "invoice_date": "YYYY-MM-DD",
 "seller": {"name": str, "gstin": str, "state": str},
 "buyer": {"name": str, "gstin": str or null, "state": str},
 "line_items": [{"description": str, "hsn": str, "quantity": number, "unit_price": number, "gst_rate": number}],
 "cgst": number, "sgst": number, "igst": number, "total_amount": number}
Use null for a missing buyer gstin. Output only the JSON.

Invoice:
"""


def norm(x):
    if isinstance(x, dict):
        return {k: norm(v) for k, v in x.items()}
    if isinstance(x, list):
        return [norm(v) for v in x]
    if isinstance(x, float):
        x = round(x, 2)
        return int(x) if x == int(x) else x
    return x


def canon(o):
    return json.dumps(norm(o), sort_keys=True, separators=(",", ":"))


def ask(prompt):
    try:
        r = requests.post(URL, json={
            "model": NAME, "temperature": 0, "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]}, timeout=600)
        text = r.json()["choices"][0]["message"]["content"]
    except Exception:
        return ""
    a, b = text.find("{"), text.rfind("}")
    if a != -1 and b > a:
        try:
            return canon(json.loads(text[a:b + 1]))
        except Exception:
            pass
    return text


rows = [json.loads(l) for l in open(TEST)][:N]
prompts = [PROMPT + r["text"] for r in rows]
with ThreadPoolExecutor(8) as ex:
    preds = list(ex.map(ask, prompts))

with open(OUT, "w") as f:
    for r, p in zip(rows, preds):
        f.write(json.dumps({"target": canon(r["label"]), "pred": p}) + "\n")

samples = [ak.Sample(input=pr, target=canon(r["label"]), actual_output=p)
           for pr, r, p in zip(prompts, rows, preds)]
result = ak.evaluate(samples, "precomputed", ["exact_match", "f1_score"])
print(f"== {NAME} on {TEST} (n={len(samples)}) ==")
print(result.summary())
