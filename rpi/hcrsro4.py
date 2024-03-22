import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
from gpiozero import DistanceSensor
import datetime

ultrasonic = DistanceSensor(echo=23, trigger=24)

# I2C bus configuration
I2C_BUS_NUMBER = 1  # Use the correct bus number obtained from i2cdetect
I2C_ADDRESS = 0x3C  # Address of the OLED display

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

# Function to turn off the display completely
def turn_off_display():
    # Clear the image buffer
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
    # Display the cleared image
    disp.image(image)
    disp.display()


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
    if distance_cm > 7:
        turn_off_display()
    
    # Wait for a short time before updating again
    time.sleep(1)
