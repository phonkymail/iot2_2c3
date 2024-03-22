import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
from gpiozero import DistanceSensor
import datetime
import RPi.GPIO as GPIO
from lib_oled96 import ssd1306
from smbus import SMBus

# GPIO setup
led_pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT)

# I2C bus configuration
I2C_BUS_NUMBER = 1  # Use the correct bus number obtained from i2cdetect
I2C_ADDRESS = 0x3C  # Address of the OLED display
i2cbus = SMBus(1)  # 1 = Raspberry Pi but NOT early REV1 board
oled = ssd1306(i2cbus)  # create oled object, nominating the correct I2C bus, default address

# Initialize display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=I2C_BUS_NUMBER, i2c_address=I2C_ADDRESS)
disp.begin()
disp.clear()
disp.display()

# Create an empty image buffer
image = Image.new("1", (disp.width, disp.height))

# Initialize font and drawing objects.
font = ImageFont.load_default()
draw = ImageDraw.Draw(image)

# Initialize ultrasonic sensor
ultrasonic = DistanceSensor(echo=23, trigger=24)

# Function to turn off the display completely
def turn_off_display():
    # Clear the image buffer
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
    # Display the cleared image
    disp.image(image)
    disp.display()

def blink():
    GPIO.output(led_pin, GPIO.HIGH)
    print("on")
    sleep(3)
    GPIO.output(led_pin, GPIO.LOW)
    print("off")

while True:
    # Clear previous text
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
    
    # Read distance from ultrasonic sensor
    distance_cm = ultrasonic.distance * 100  # Convert distance to centimeters
    
    # Get current date and time
    current_time = datetime.datetime.now()
    
    # Draw distance on the display
    draw.text((0, 0), "Distance: {:.2f} cm".format(distance_cm), font=font, fill=255)
    
    # Draw date and time on the display
    draw.text((0, 20), "Date: {}".format(current_time.strftime("%d-%m-%Y")), font=font, fill=255)
    draw.text((0, 40), "Time: {}".format(current_time.strftime("%H:%M:%S")), font=font, fill=255)

    # Display the image
    disp.image(image)
    disp.display()
    
    # Check if distance is above 5 cm and turn off the display if so
    if distance_cm < 5:
        blink()
        # put border around the screen:
        oled.canvas.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
        led_status = "on" if GPIO.input(led_pin) == GPIO.HIGH else "off"
        oled.canvas.text((40, 15), f'LED is {led_status}', fill=1)
        oled.canvas.text((40, 40), f'Distance: {distance_cm:.2f} cm', fill=1)
        # now display that canvas out to the hardware
        oled.display()
    else:
        turn_off_display()

    # Wait for a short time before updating again
    time.sleep(1)
