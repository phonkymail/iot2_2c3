from machine import Pin, ADC, Timer
import utime
from time import sleep

# Pins
flame = Pin(22, Pin.IN)
knust = Pin(26, Pin.IN)
water = ADC(Pin(35))
pir = Pin(5, Pin.IN)
bat = ADC(Pin(34))

# LED Pin
led_pin = Pin(14, Pin.OUT)

# Set attenuation for ADC
bat.atten(ADC.ATTN_11DB)
water.atten(ADC.ATTN_11DB)

# Initialize variables to store previous sensor values
prev_flame_value = flame.value()
prev_knust_value = knust.value()
prev_water_value = water.read()  # Initial value for analog sensor
prev_pir_value = pir.value()
prev_bat_value = bat.read()

def toggle_led():
    led_pin.value(1)
    sleep(0.05)
    led_pin.value(0)
    sleep(5)



# Function to read flame sensor value
def read_flame(timer):
    global prev_flame_value
    flame_value = flame.value()
    if flame_value != prev_flame_value:
        print("Flame Sensor:", flame_value)
        prev_flame_value = flame_value

# Set up timer for flame sensor with tick_ms
flame_timer = Timer(2)
flame_timer.init(period=1000, mode=Timer.PERIODIC, callback=read_flame)

# Function to read knust sensor value
def read_knust(timer):
    global prev_knust_value
    knust_value = knust.value()
    if knust_value != prev_knust_value:
        print("Knust Sensor:", knust_value)
        prev_knust_value = knust_value

# Set up timer for knust sensor with tick_ms
knust_timer = Timer(3)
knust_timer.init(period=1000, mode=Timer.PERIODIC, callback=read_knust)

# Function to read PIR sensor value
def read_pir(timer):
    global prev_pir_value
    pir_value = pir.value()
    if pir_value != prev_pir_value:
        print("PIR Sensor:", pir_value)
        prev_pir_value = pir_value

# Set up timer for PIR sensor with tick_ms
pir_timer = Timer(4)
pir_timer.init(period=1000, mode=Timer.PERIODIC, callback=read_pir)

# Water sensor

# Function to read water sensor value
def read_water(timer):
    global prev_water_value
    water_value = water.read()

    if water_value != prev_water_value:
        if water_value == 0:
            print("Water Sensor: 0")
        elif 0 < water_value <= 1000:
            # Calculate and print the average value
            average_value = water_value
            print("Water Sensor: Average =", average_value)
        else:
            # Print high value
            print("Water Sensor: High =", water_value)

        # Update previous value
        prev_water_value = water_value

# Set up timer for water sensor with tick_ms
water_timer = Timer(5)
water_timer.init(period=1000, mode=Timer.PERIODIC, callback=read_water)

# Battery

# Function to read battery voltage
def read_bat(timer):
    global prev_bat_value

    sum_bat_value = 0
    num_measurements = 50

    for _ in range(num_measurements):
        sum_bat_value += bat.read()

    average_bat_value = sum_bat_value // num_measurements
    
    if average_bat_value != prev_bat_value:
        print("Average Battery Voltage (ADC):", average_bat_value)
        prev_bat_value = average_bat_value

# Set up timer for battery voltage with tick_ms
bat_timer = Timer(6)
bat_timer.init(period=3000, mode=Timer.PERIODIC, callback=read_bat)

# Main loop
while True:
    toggle_led()
    utime.sleep(0.1)


