#!/usr/bin/env bash

set -e
set -u

if [[ -d ~/.config/gemini/server/venv ]]; then
    exit 0
fi

python3 -m venv ~/.config/gemini/server/venv
source ~/.config/gemini/server/venv/bin/activate
pip install wheel
pip install -r requirements.txt
