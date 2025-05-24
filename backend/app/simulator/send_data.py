import requests
import random
import time
import json

URL = "http://localhost:8000/data"

COMMANDS = ["open_window", "close_window", "activate_alarm"]

def send_random_data():
    while True:
        payload = {
            "command": random.choice(COMMANDS),
            "source": "simulator",
            "value": random.randint(0, 100),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        response = requests.post(URL, json=payload)
        print("Sent:", payload, "| Status:", response.status_code)
        time.sleep(5)

if __name__ == "__main__":
    send_random_data()
