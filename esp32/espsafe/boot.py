import network
import time

# Replace the SSID/Password details as per your wifi router
ssid = "ravdesktop"
password = "gedser73"

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
    
connect_wifi()
