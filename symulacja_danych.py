# symulator.py
import random
import time
import requests

def generate_sensor_data():
    temperature = random.uniform(15.0, 30.0)  # temperatura w stopniach Celsjusza
    humidity = random.uniform(30.0, 70.0)     # wilgotność w procentach
    co2_level = random.uniform(300, 1000)     # poziom CO2 w ppm
    return {
        "temperature": temperature,
        "humidity": humidity,
        "co2_level": co2_level
    }

def send_data_to_api(data):
    api_url = "http://<twoje-api-url>/window/status"
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        print(f"Dane zostały wysłane: {data}")
    else:
        print("Błąd przy wysyłaniu danych")

while True:
    data = generate_sensor_data()
    send_data_to_api(data)
    time.sleep(5)  # Czas oczekiwania przed kolejną symulacją