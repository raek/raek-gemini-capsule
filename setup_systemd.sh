#!/usr/bin/env bash

set -e
set -u

systemctl --user disable --now gemini.service 2>/dev/null || true
systemctl --user daemon-reload
systemctl --user link "$(pwd)"/gemini.service
systemctl --user enable --now gemini.service
