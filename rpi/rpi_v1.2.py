import paho.mqtt.client as mqtt
import json
import time

# MQTT Broker details (Flespi)
mqtt_server_receiver = "127.0.0.1"
mqtt_server_sender = "20.93.22.213"

# Function to connect to MQTT receiver server
def connect_mqtt_receiver():
    client = mqtt.Client("ESP32_receiver")
    client.on_message = on_message  # Assign on_message callback here

    while True:
        try:
            client.connect(mqtt_server_receiver)
            print("Connected to MQTT receiver server.")
            client.subscribe("espsafe/pir")
            client.subscribe("espsafe/flame")  # Subscribe to flame sensor topic
            client.subscribe("espsafe/water")  # Subscribe to water sensor topic
            client.subscribe("espsafe/knust")
            client.subscribe("espsafe/bat")   # Subscribe to knust sensor topic
            break
        except Exception as e:
            print("Failed to connect to MQTT receiver server. Retrying...")
            print(e)
            time.sleep(2)

    return client

# Function to connect to MQTT sender server
def connect_mqtt_sender():
    client = mqtt.Client("ESP32_sender")

    while True:
        try:
            client.connect(mqtt_server_sender)
            print("Connected to MQTT sender server.")
            break
        except Exception as e:
            print("Failed to connect to MQTT sender server. Retrying...")
            print(e)
            time.sleep(2)

    return client

# Callback function to handle incoming MQTT messages
def on_message(client, userdata, message):
    print("Received message on topic:", message.topic)
    print("Message:", message.payload.decode())
    forward_message_to_another_broker(message.payload)

# Function to forward received message to another MQTT broker
def forward_message_to_another_broker(msg):
    global sender_client
    sender_client.publish("espsafe/pir", msg)

# Main function
def main():
    receiver_client = connect_mqtt_receiver()
    global sender_client
    sender_client = connect_mqtt_sender()

    while True:
        receiver_client.loop()
        time.sleep(1)

if __name__ == "__main__":
    main()
