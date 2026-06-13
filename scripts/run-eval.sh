#!/bin/bash
set -e

INTERVAL=${EVAL_INTERVAL:-3600}

source /app/.venv/bin/activate

while true; do
    echo "[$(date)] Starting evaluation run..."
    python -m evals.main
    echo "[$(date)] Run complete. Sleeping ${INTERVAL}s..."
    sleep "$INTERVAL"
done