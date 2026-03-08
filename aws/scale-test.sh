#!/bin/bash
# Install stress utility and run CPU load test
sudo apt install -y stress
stress --cpu 4 --timeout 180
