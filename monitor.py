import subprocess
import pandas as pd
import datetime
import time
import smtplib
import os
import json
import logging
from email.mime.text import MIMEText
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ==========================
# LOAD CONFIGURATION
# ==========================

try:
    with open("config.json") as config_file:
        config = json.load(config_file)
        INTERVAL = config["interval"]
        THRESHOLD_LATENCY = config["latency_threshold"]
except Exception:
    print("Error loading config.json. Using default values.")
    INTERVAL = 10
    THRESHOLD_LATENCY = 100

# ==========================
# EMAIL CONFIGURATION
# ==========================

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

# ==========================
# DEVICE STATUS MEMORY
# ==========================

device_status_memory = {}

# ==========================
# LOGGING SETUP
# ==========================

logging.basicConfig(
    filename="system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================
# PING FUNCTION
# ==========================

def ping_device(ip):
    try:
        output = subprocess.check_output(
            ["ping", "-n", "1", ip],
            universal_newlines=True
        )

        if "TTL=" in output:
            latency = output.split("time=")[-1].split("ms")[0]
            latency = latency.replace("<", "").strip()
            return "UP", latency
        else:
            return "DOWN", None

    except subprocess.CalledProcessError:
        return "DOWN", None
    except Exception:
        return "DOWN", None

# ==========================
# CSV LOGGING FUNCTION
# ==========================

def log_data(ip, status, latency):
    current_time = datetime.datetime.now()

    df = pd.DataFrame(
        [[current_time, ip, status, latency]],
        columns=["Time", "IP", "Status", "Latency"]
    )

    file_exists = os.path.isfile("logs.csv")

    df.to_csv(
        "logs.csv",
        mode="a",
        header=not file_exists,
        index=False
    )

# ==========================
# EMAIL ALERT FUNCTION
# ==========================

def send_email_alert(ip):
    try:
        subject = f"ALERT: Device {ip} is DOWN"
        body = f"The device with IP {ip} is not responding."

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print(Fore.YELLOW + f"Email alert sent for {ip}")
        logging.warning(f"Email alert sent for {ip}")

    except Exception as e:
        print(Fore.RED + f"Failed to send email alert: {e}")
        logging.error(f"Email failed for {ip}: {e}")

# ==========================
# MONITOR FUNCTION
# ==========================

def monitor():
    try:
        with open("devices.txt") as file:
            devices = file.read().splitlines()
    except FileNotFoundError:
        print(Fore.RED + "devices.txt file not found!")
        return

    print(Fore.CYAN + "Starting Smart Network Monitor...\n")

    while True:
        print(Fore.CYAN + "Checking devices...\n")

        for ip in devices:
            status, latency = ping_device(ip)

            # ======================
            # DEVICE IS UP
            # ======================
            if status == "UP":
                print(Fore.GREEN + f"{ip} is UP | Latency: {latency} ms" + Style.RESET_ALL)
                logging.info(f"{ip} is UP with latency {latency}")
                log_data(ip, "UP", latency)

                device_status_memory[ip] = "UP"

                if latency:
                    latency_value = int(latency)
                    if latency_value > THRESHOLD_LATENCY:
                        print(Fore.YELLOW + f"High latency detected for {ip}!")
                        logging.warning(f"High latency detected for {ip}")

            # ======================
            # DEVICE IS DOWN
            # ======================
            else:
                print(Fore.RED + f"{ip} is DOWN" + Style.RESET_ALL)
                logging.warning(f"{ip} is DOWN")
                log_data(ip, "DOWN", None)

                # Smart Alert Logic (avoid spam)
                if device_status_memory.get(ip) != "DOWN":
                    send_email_alert(ip)

                device_status_memory[ip] = "DOWN"

        print("\n--------------------------------------\n")
        time.sleep(INTERVAL)

# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    monitor()
