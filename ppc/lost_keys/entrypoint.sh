#!/bin/sh

cd /app

echo "[*] Starting socat..."
socat TCP4-LISTEN:1337,reuseaddr,fork EXEC:./server.py