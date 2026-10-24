#!/bin/bash
# usage: serve2.sh <model-path-or-hf-id> <served-name>
source ~/ps5/.venv/bin/activate
sglang serve \
  --model-path "$1" \
  --served-model-name "$2" \
  --port 30000 \
  --context-length 4096 \
  --mem-fraction-static 0.6 \
  --attention-backend triton \
  --sampling-backend pytorch
