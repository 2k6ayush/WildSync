#!/usr/bin/env bash
set -euo pipefail

# Optional wait for a host/port (e.g., Postgres)
python - <<'PY'
import os, socket, time
host=os.environ.get('WAIT_FOR_HOST')
port=os.environ.get('WAIT_FOR_PORT')
if host and port:
    port=int(port)
    print(f"Waiting for {host}:{port}...")
    for i in range(180):
        try:
            with socket.create_connection((host, port), timeout=1):
                print("Target is up")
                break
        except OSError:
            time.sleep(1)
PY

# Start gunicorn
exec gunicorn -w "${GUNICORN_WORKERS:-4}" -k gthread --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" -b 0.0.0.0:8000 backend.wsgi:app
