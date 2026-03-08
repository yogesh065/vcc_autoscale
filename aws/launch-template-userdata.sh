#!/bin/bash
apt-get update -y
apt-get install -y python3 python3-pip python3-venv

mkdir -p /opt/hybrid-fastapi-app
cd /opt/hybrid-fastapi-app

cat <<'EOF' > main.py
from fastapi import FastAPI
from datetime import datetime
import socket
import os

app = FastAPI(title="Hybrid FastAPI AutoScale Demo")

HOSTNAME = socket.gethostname()
ENVIRONMENT = os.getenv("APP_ENV", "aws-cloud")

@app.get("/")
def root():
    return {
        "message": "Hybrid FastAPI AutoScale Demo",
        "environment": ENVIRONMENT,
        "hostname": HOSTNAME,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cpu-test")
def cpu_test():
    total = 0
    for i in range(10_000_000):
        total += i * i
    return {"message": "CPU load test complete", "result": total}
EOF

cat <<'EOF' > requirements.txt
fastapi
uvicorn[standard]
EOF

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cat <<'EOF' > /etc/systemd/system/hybrid-fastapi.service
[Unit]
Description=Hybrid FastAPI Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/hybrid-fastapi-app
Environment=APP_ENV=aws-cloud
ExecStart=/opt/hybrid-fastapi-app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable hybrid-fastapi.service
systemctl start hybrid-fastapi.service
