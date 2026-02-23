# Smart Network Monitoring & Alert System

## Overview
A Python-based network monitoring tool designed to simulate enterprise-level infrastructure monitoring. The system tracks device availability, measures latency, logs performance metrics, and generates alerts for downtime detection.

## Features
- Multi-device monitoring
- Real-time latency tracking
- CSV-based logging
- Automated email alerts
- Performance visualization dashboard
- Continuous monitoring loop

## Technologies Used
- Python
- Pandas
- Matplotlib
- SMTP (Email Alerts)
- Subprocess (System Ping)

## Project Architecture
1. Reads IP addresses from devices.txt
2. Pings each device
3. Logs availability and latency to logs.csv
4. Sends alert if device is down
5. Generates performance graphs using visualize.py

## How to Run

### Install Dependencies
pip install -r requirements.txt

### Start Monitoring
python monitor.py

### Visualize Performance
python visualize.py

## Use Case
Designed to simulate industrial and enterprise network monitoring environments where system availability and performance tracking are critical.

## Future Improvements
- Multi-threaded monitoring
- Real-time dashboard using Flask
- Packet loss tracking
- Deployment as background service
