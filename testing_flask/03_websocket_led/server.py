from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

led_pin = 26

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('button_pressed')
def handle_button_press(data):
    button = data.get('button')
    if button == 'on':
        print('Button on pressed')
        GPIO.output(led_pin, GPIO.HIGH)
        emit('response', 'LED ON')
    elif button == 'off':
        print('Button off pressed')
        GPIO.output(led_pin, GPIO.LOW)
        emit('response', 'LED OFF')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

    #GPIO Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)
