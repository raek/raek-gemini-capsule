#!/usr/bin/env bash

set -e
set -u

mkdir -p ~/.config/gemini/server
./mkcert.sh
./mkvenv.sh
./setup_systemd.sh
