from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(580, GPIO.OUT)

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('button_pressed')
def handle_button_press(data): 
    print(f"Button pressed: {data}")  # Receive and print the button's value

    if data == 1:
        GPIO.output(580, GPIO.HIGH)
    else:
        GPIO.output(580, GPIO.LOW)

    emit('response', {'message': f"Button {data} pressed!"})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='192.168.1.207', port=5000)

    #app.run(host='0.0.0.0', port=5000)