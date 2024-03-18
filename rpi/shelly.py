import requests
import RPi.GPIO as GPIO
from time import sleep

# Adres IP 
ip_address = "192.168.137.164"

# Pin GPIO 
button_pin = 26


GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

relay_state = False  

def control_relay(turn):

    url = f"http://{ip_address}/relay/0?turn={turn}"
    response = requests.get(url)
    return response.status_code == 200

def get_relay_state():

    url = f"http://{ip_address}/relay/0"
    response = requests.get(url)
    return response.text

try:
    while True:
      
        button_state = GPIO.input(button_pin)

      
        if button_state == GPIO.LOW:
            if not relay_state:  
                success = control_relay("on")
                if success:
                    print("turn on")
                    relay_state = True
                else:
                    print("cannot turn on")
            else:  
                success = control_relay("off")
                if success:
                    print("Pturn off")
                    relay_state = False
                else:
                    print("cannot turn off")

        
            sleep(0.2)

        sleep(0.1)

except KeyboardInterrupt:
    print("\nquit")

finally:
    GPIO.cleanup()
