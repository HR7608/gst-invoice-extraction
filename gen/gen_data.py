import json
import os
import random

from invoice import make_invoice
from render import render


def build(n, path, seed):
    random.seed(seed)
    rows = []
    rejected = 0
    while len(rows) < n:
        inv = make_invoice()
        if inv["seller"]["name"] == inv["buyer"]["name"]:
            rejected += 1
            continue
        rows.append({"text": render(inv), "label": inv})
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{path}: {len(rows)} rows, {rejected} rejected")


if __name__ == "__main__":
    os.makedirs("../data", exist_ok=True)
    build(3000, "../data/train.jsonl", seed=42)
    build(300, "../data/test.jsonl", seed=7)
