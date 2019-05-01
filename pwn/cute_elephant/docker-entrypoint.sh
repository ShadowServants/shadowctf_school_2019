#!/bin/sh

service postgresql start

echo "[*] Starting socat..."
socat TCP4-LISTEN:7777,reuseaddr,fork EXEC:"runuser -l postgres -c 'psql'",stderr