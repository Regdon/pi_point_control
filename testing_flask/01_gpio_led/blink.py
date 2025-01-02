# Script to blink an LED attached to GPIO Pin xx on a Raspberry Pi
# LED PIN 18, Button PIN 23


import RPi.GPIO as GPIO
import time

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO 18 as an output pin
led_pin = 18
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
        time.sleep(1)                    # Wait 1 second
        GPIO.output(led_pin, GPIO.LOW)   # Turn LED off
        time.sleep(1)                    # Wait 1 second

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # Clean up GPIO settings
