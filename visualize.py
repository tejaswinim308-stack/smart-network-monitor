import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("logs.csv")

data = data[data["Status"] == "UP"]

data["Time"] = pd.to_datetime(data["Time"])


for ip in data["IP"].unique():
    ip_data = data[data["IP"] == ip]
    plt.plot(ip_data["Time"], ip_data["Latency"], label=ip)

plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Latency (ms)")
plt.title("Network Performance Monitoring")
plt.legend()
plt.tight_layout()
plt.show()
