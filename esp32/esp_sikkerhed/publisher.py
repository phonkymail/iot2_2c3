import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
import random


# Function to connect to WiFi
def connect_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)

    print("Connected to WiFi.")
    print("IP Address:", station.ifconfig()[0])
    
    
# Default MQTT server to connect to
SERVER = "192.168.137.97"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"esp/temperature"

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    
def main():
    mqttClient = MQTTClient(CLIENT_ID, SERVER, keepalive=60)
    mqttClient.connect()
    print(f"Connected to MQTT  Broker :: {SERVER}")

    while True:
        random_temp = random.randint(20, 50)
        print(f"Publishing temperature :: {random_temp}")
        mqttClient.publish(TOPIC, str(random_temp).encode())
        time.sleep(3)
    mqttClient.disconnect()
    
    
if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()
