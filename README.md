# Hybrid FastAPI AutoScale

Hybrid Auto-Scaling from Local VM to AWS Cloud Using FastAPI.

## Project Structure

```
hybrid-fastapi-autoscale/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── monitor/
│   ├── config.py
│   └── cpu_monitor.py
└── aws/
    ├── launch-template-userdata.sh
    └── scale-test.sh
```

## Setup

### Local VM (Ubuntu)

```bash
cd app/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Monitor

```bash
cd monitor/
python3 cpu_monitor.py
```

### Load Test

```bash
bash aws/scale-test.sh
```

## Configuration

Edit `monitor/config.py` to set:
- `AWS_REGION`
- `AUTO_SCALING_GROUP_NAME`
- `CPU_THRESHOLD` (default: 75%)
- `CONSECUTIVE_BREACHES` (default: 12 = ~2 minutes)
