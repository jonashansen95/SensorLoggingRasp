#!/usr/bin/python
import Adafruit_DHT
import requests
import numpy


def evaluate(value, list, allowedOffset):
    if value < numpy.average(list) - allowedOffset:
        return False
    if value > numpy.average(list) + allowedOffset:
        return False
    return value


url = "https://api.joerha.dk/climate"
headers = {"X-API-Key": "d2c9c21f077d65cfe53388a976764472"}

humidityList = []
temperatureList = []
size = 30
first = True
while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    temperature = evaluate(temperature, temperatureList, 10)
    humidity = evaluate(humidity, humidityList, 20)

    if temperature and humidity or first:
        first = False
        humidityList.append(humidity)
        temperatureList.append(temperature)
        if len(humidityList) > size:
            humidityList.pop(0)
        if len(temperatureList) > size:
            temperatureList.pop(0)
        payload = {"temp": temperature, "humidity": humidity}

        r = requests.post(url, headers=headers, data=payload)
        print(r.status_code)
