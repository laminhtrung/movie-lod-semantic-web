#!/bin/zsh
set -e
cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
  .venv/bin/python -m pip install -r requirements.txt
fi
print 'Mở trình duyệt tại http://127.0.0.1:8000'
.venv/bin/python src/server.py
