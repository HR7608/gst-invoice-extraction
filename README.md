# GSTrack: a 1.5B model, trained on a laptop, that turns messy GST invoices into schema-valid JSON

*Syntax Error 2026, Local LLM Track, PS 5: Structured output and extraction.*

Turns messy Indian GST invoice text into schema-valid JSON. Qwen2.5-1.5B-Instruct is fine-tuned with QLoRA on a laptop RTX 4060 (8 GB), served with SGLang, and scored with AuditKit.

## Results (AuditKit, n=100 per set, greedy decoding)

| Test set | Base exact match | Fine-tuned exact match | Base F1 | Fine-tuned F1 |
|---|---|---|---|---|
| Layouts A/B (seen in training) | 5% | **99%** | 0.34 | 0.99 |
| Layout C (unseen layout) | 1% | **99%** | 0.35 | 1.00 |
| Out-of-distribution (unseen layouts, companies, products, HSN codes, 0%/28% rates, new states) | 3% | **100%** | 0.47 | 1.00 |

Exact match = the whole invoice (canonicalised JSON) is correct. F1 is AuditKit's text-overlap score on that JSON string.
Predictions are in `results/pred_*.jsonl`.

## Pipeline (Lexsi toolchain + SGLang)

1. **Data (CuratorKit):** `gen/invoice.py` builds ground-truth invoices first (real GSTIN checksum, CGST+SGST for same-state and IGST for different-state, totals computed). `gen/render.py` turns them into messy text in 2 layouts with OCR-style noise. 3,000 training rows were passed through CuratorKit (schema gate, exact + MinHash dedup, cleaning): 3,000 passed, 0 rejected, because the labels are correct by construction. The manifest and checksums are in `results/`.
2. **Fine-tuning (AlignTune, TRL backend):** QLoRA (4-bit base, LoRA r=16, alpha=32, all linear layers), lr 2e-4, 1 epoch, 1,000 examples, batch size 1, max length 2048. About 45 minutes on the 8 GB laptop GPU.
3. **Serving and evaluation (SGLang + AuditKit):** the merged model is served with SGLang (`serve2.sh`); AuditKit scores the predictions (`gen/ak_eval.py`).

## Reproduce

Scripts use relative paths (`../data`), so run them from inside `gen/`. Model and output paths in `train_full.py` are those of the author's machine; edit them.

```
cd gen
python3 gen_data.py                  # writes ../data/train.jsonl, test.jsonl
python3 gen_test_c.py && python3 gen_test_ood.py
python3 to_alpaca.py && python3 curate.py
python3 train_full.py                # AlignTune SFT (QLoRA)
python3 merge_lora.py OUT_DIR MERGED_DIR
../serve2.sh MERGED_DIR ft           # SGLang server (port 30000)
python3 ak_eval.py ft ../data/test.jsonl
```

Sample data is in `data_samples/`; predictions and CuratorKit manifests are in `results/`.

## Limitations (please read)

- All training and test data is **synthetic**. The out-of-distribution test uses the same generator code with new entity lists, so it does not show performance on real scanned invoices.
- One hand-written invoice in a format outside the generator was extracted correctly (`gen/invoice_real.txt`). This is an anecdote, not a measurement.
- n=100 per test set and a single training run: no variance estimate.
- Invoices have 1-5 line items. English only. No OCR step: input is already text.
- The model copies GSTINs but does not verify checksums; use `gen/gstin.py:is_valid_gstin` as a post-check.
