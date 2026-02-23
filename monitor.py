import subprocess
import pandas as pd
import datetime

def ping_device(ip):
    try:
        output = subprocess.check_output(["ping", "-n", "1", ip], universal_newlines=True)
        if "TTL=" in output:
            latency = output.split("time=")[-1].split("ms")[0].replace("<", "").strip()
            return "UP", latency
        else:
            return "DOWN", None
    except:
        return "DOWN", None

with open("devices.txt") as file:
    devices = file.read().splitlines()

for ip in devices:
    status, latency = ping_device(ip)
    print(ip, status, latency)

    time = datetime.datetime.now()

    df = pd.DataFrame([[time, ip, status, latency]],
                      columns=["Time", "IP", "Status", "Latency"])

    df.to_csv("logs.csv", mode="a", header=not pd.io.common.file_exists("logs.csv"), index=False)