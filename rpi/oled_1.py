import RPi.GPIO as GPIO
from lib_oled96 import ssd1306
from time import sleep

# GPIO setup
led_pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)

def blink():
    GPIO.output(led_pin, GPIO.HIGH)
    print("on")
    sleep(3)
    GPIO.output(led_pin, GPIO.LOW)
    print("off")

# OLED setup
from smbus import SMBus
i2cbus = SMBus(1)  # 1 = Raspberry Pi but NOT early REV1 board
oled = ssd1306(i2cbus)  # create oled object, nominating the correct I2C bus, default address

# we are ready to do some output ...
# put border around the screen:
oled.canvas.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)

# Write two lines of text.
led_status = "on" if GPIO.input(led_pin) == GPIO.HIGH else "off"
oled.canvas.text((40, 15), f'LED is {led_status}', fill=1)
oled.canvas.text((40, 40), 'rafal', fill=1)

# now display that canvas out to the hardware
oled.display()
sleep(3)
oled.onoff(0)

# Cleanup GPIO
GPIO.cleanup()
