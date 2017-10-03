#!/usr/bin/python
import Adafruit_DHT
import requests

url = "https://joerha.dk/climate"
headers = {"X-API-Key": "d2c9c21f077d65cfe53388a976764472"}

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    payload = {"temp": temperature, "humidity": humidity}

    r = requests.post(url, headers=headers, data=payload)
    print(r.status_code)
