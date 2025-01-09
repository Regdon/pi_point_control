#Import for i2c
import smbus

#Import for Websocket & server
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialize the I2C bus
bus = smbus.SMBus(1)

# I2C address of the Arduino
ARDUINO_ADDRESS = 0x08

def read_from_arduino():
    data = bus.read_i2c_block_data(ARDUINO_ADDRESS, 0, 16)
    return ''.join(chr(i) for i in data)

def write_to_arduino(value):
    bus.write_i2c_block_data(ARDUINO_ADDRESS, 0, [ord(c) for c in value])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('button_pressed')
def handle_button_press(data):
    button = data.get('button')
    if button == 'on':
        print('Button on pressed')
        write_to_arduino('on')
        emit('response', 'LED ON')
    elif button == 'off':
        print('Button off pressed')
        write_to_arduino('off')
        emit('response', 'LED OFF')

if __name__ == '__main__':
    #Run server
    socketio.run(app, host='0.0.0.0', port=5000)