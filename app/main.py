from fastapi import FastAPI
from datetime import datetime
import socket
import os

app = FastAPI(title="Hybrid FastAPI AutoScale Demo")

HOSTNAME = socket.gethostname()
ENVIRONMENT = os.getenv("APP_ENV", "local-vm")

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
