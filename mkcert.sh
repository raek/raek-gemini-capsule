#!/usr/bin/env bash

set -u
set -e

cd ~/.config/gemini/server/

if [[ ! -f privkey.pem ]]; then
    echo Creating private key
    openssl genrsa -out privkey.pem 2048
fi

if [[ ! -f cert.pem ]]; then
    echo Creating certificate
    openssl req -x509 \
	    -out cert.pem \
	    -key privkey.pem \
	    -subj "/CN=raek.se" \
	    -addext "subjectAltName = DNS:raek.se,DNS:*.raek.se,DNS:xn--rk-via.se,DNS:*.xn--rk-via.se" \
	    -days $((365 * 5))
fi

#openssl x509 -in cert.pem -noout -text
