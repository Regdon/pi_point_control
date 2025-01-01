from flask import Flask, render_template
from flask_socketio import SocketIO, emit
#import RPi.GPIO as GPIO
from gpiozero.pins.lgpio import LGPIOFactory

from gpiozero import LED
from gpiozero import Device
from time import sleep


def main()
    factory = LGPIOFactory(chip=0)
    Device.pin_factory = factory


    print(Device.pin_factory)

    sleep(0.1)
    try:
        led = LED(6)
        print("Set up pin 6")
    except:
        print("Could not initilse pin 6")

    sleep(0.1)

    app = Flask(__name__)
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('button_pressed')
    def handle_button_press(data): 
        print(f"Button pressed: {data}")  # Receive and print the button's value

        if data == 1:
            led.on()
        else:
            led.off()

        sleep(0.1)
        emit('response', {'message': f"Button {data} pressed!"})

if __name__ == '__main__':
    print("setting up")
    socketio.run(app, debug=True, host='192.168.1.207', port=5000)
    main()

    #app.run(host='0.0.0.0', port=5000)