import paho.mqtt.client as mqtt
import time

# MQTT Broker details
mqtt_server_receiver = "127.0.0.1"
mqtt_server_sender = "74.234.16.173"

# Function to connect to MQTT receiver server
def connect_mqtt_receiver():
    client = mqtt.Client("ESP32_air")
    client.on_message = on_message_receiver

    while True:
        try:
            client.connect(mqtt_server_receiver)
            print("Connected to MQTT receiver server.")
            client.subscribe("espluft/dht")
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

# Callback function to handle incoming MQTT messages for receiver
def on_message_receiver(client, userdata, message):
    print("Received message on topic:", message.topic)
    print("Message:", message.payload.decode())
    forward_message_to_another_broker(message.payload)

# Function to forward received message to another MQTT broker
def forward_message_to_another_broker(msg):
    global sender_client
    sender_client.publish("espair/dht", msg)

# Main function
def main():
    global sender_client
    receiver_client = connect_mqtt_receiver()
    sender_client = connect_mqtt_sender()

    while True:
        receiver_client.loop()
        time.sleep(1)

if __name__ == "__main__":
    main()
