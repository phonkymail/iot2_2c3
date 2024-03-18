import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
import dht
import json

# Default MQTT server to connect to
SERVER = "192.168.137.129"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"espair/dht"

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    
def read_dht():
    dht_sensor = dht.DHT11(machine.Pin(19))
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

def main():
    mqttClient = MQTTClient(CLIENT_ID, SERVER, keepalive=60)
    mqttClient.connect()
    print(f"Connected to MQTT Broker: {SERVER}")

    while True:
        temperature, humidity = read_dht()
        print(f"Temperature: {temperature}, Humidity: {humidity}")
        mqttClient.publish(TOPIC, json.dumps({"temperature": temperature, "humidity": humidity}))
        time.sleep(3)
    mqttClient.disconnect()
    
    
if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()

