# LED PIN 26, Button PIN 19

import RPi.GPIO as GPIO
import time

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO 17 as an output pin (for the LED)
led_pin = 26
GPIO.setup(led_pin, GPIO.OUT)

# Set GPIO 23 as an input pin (for the button) with an internal pull-down resistor
button_pin = 19
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # Read the state of the button
        button_state = GPIO.input(button_pin)

        if button_state == GPIO.HIGH:
            # Button is pressed
            GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
        else:
            # Button is not pressed
            GPIO.output(led_pin, GPIO.LOW)   # Turn LED off

        time.sleep(0.1)  # Debounce delay

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # Clean up GPIO settings
