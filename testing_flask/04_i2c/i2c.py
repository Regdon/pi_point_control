import smbus
import time

# Initialize the I2C bus
bus = smbus.SMBus(1)

# I2C address of the Arduino
ARDUINO_ADDRESS = 0x08

def read_from_arduino():
    data = bus.read_i2c_block_data(ARDUINO_ADDRESS, 0, 16)
    return ''.join(chr(i) for i in data)

def write_to_arduino(value):
    bus.write_i2c_block_data(ARDUINO_ADDRESS, 0, [ord(c) for c in value])

while True:
    # Write a message to the Arduino
    write_to_arduino("Ping")

    # Read the response from the Arduino
    response = read_from_arduino()
    print(f"Received from Arduino: {response}")

    # Wait before the next operation
    time.sleep(1)
