#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x ".venv/bin/python" ]]; then
  python3 -m venv .venv
fi

./.venv/bin/python -m pip install -r app/backend/requirements.txt

echo "Run the backend with:"
echo "  PYTHONPATH=app/backend ./.venv/bin/uvicorn app.main:app --reload"
echo
echo "Run the frontend with:"
echo "  python3 -m http.server 3000 -d app/frontend"
echo
echo "Seed demo data with:"
echo "  PYTHONPATH=app/backend ./.venv/bin/python -m app.seed"
