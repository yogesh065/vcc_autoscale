import time
import subprocess
import logging
from config import (
    AWS_REGION,
    AUTO_SCALING_GROUP_NAME,
    CPU_THRESHOLD,
    CHECK_INTERVAL,
    CONSECUTIVE_BREACHES,
    DESIRED_CAPACITY,
    LOG_FILE,
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

high_count = 0
scaled = False

def get_cpu_usage():
    cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print 100 - $8}'"
    result = subprocess.check_output(cmd, shell=True).decode().strip()
    try:
        return float(result)
    except Exception:
        return 0.0

def scale_out():
    command = [
        "aws", "autoscaling", "set-desired-capacity",
        "--region", AWS_REGION,
        "--auto-scaling-group-name", AUTO_SCALING_GROUP_NAME,
        "--desired-capacity", str(DESIRED_CAPACITY),
        "--honor-cooldown"
    ]
    subprocess.run(command, check=True)

def main():
    global high_count, scaled

    while True:
        cpu = get_cpu_usage()
        logging.info(f"CPU usage: {cpu:.2f}%")

        if cpu > CPU_THRESHOLD:
            high_count += 1
            logging.warning(f"High CPU: {high_count}/{CONSECUTIVE_BREACHES}")
        else:
            high_count = 0

        if high_count >= CONSECUTIVE_BREACHES and not scaled:
            logging.warning("Threshold exceeded. Triggering scale-out.")
            try:
                scale_out()
                scaled = True
                logging.info("Scale-out completed successfully.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Scale-out failed: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
