import network
import time
from machine import Pin
from time import sleep

# Replace the SSID/Password details as per your wifi router
ssid = "ravdesktop"
password = "gedser73"

led_pin = Pin(14, Pin.OUT)

def toggle_led(x):
    led_pin.value(1)
    sleep(x)
    led_pin.value(0)

    
    
# Function to connect to WiFi
def connect_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        print("Connecting to WiFi...")
        toggle_led(0.3)
        sleep(1)

    print("Connected to WiFi.")
    print("IP Address:", station.ifconfig()[0])  
connect_wifi()
