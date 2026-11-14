# Lab 8: Publisher
# Liam Tuite - c21447352
# Oisin Kiely - c21501436
# Providence Obiozor - c20499732

import network
import machine
import time
from umqtt.simple import MQTTClient

# WiFi and MQTT Broker Configuration - Fill with correct details
WIFI_NAME= "WIFI"
WIFI_PASSWORD= "PASSWORD"
BROKER_IP = "IP_ADDRESS"

sensor = machine.ADC(4)

# Function to read temperature from the sensor
#converts the raw ADC value to voltage and then to temperature in Celsius
def read_temperature():
    value = sensor.read_u16()
    voltage = value * (3.3 / 65536)
    temperature = 27 - (voltage - 0.706) /0.001721
    return temperature

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  
wlan.connect(WIFI_NAME, WIFI_PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print("Connected to WiFi")
print("IP Address:", wlan.ifconfig()[0])
# Connect to MQTT Broker
client = MQTTClient("publisher", BROKER_IP)
client.connect()
print("Connected to MQTT Broker")
# Publish temperature readings to the MQTT topic "temperature/pico" every second
while True:
    temperature = read_temperature()
    message = str(round(temperature, 2))
    client.publish(b"temperature/pico", message.encode())
    time.sleep(1)
