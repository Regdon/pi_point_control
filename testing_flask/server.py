from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('button_pressed')
def handle_button_press(data): 
    print(f"Button pressed: {data}")  # Receive and print the button's value
    emit('response', {'message': f"Button {data} pressed!"})

if __name__ == '__main__':
    socketio.run(app, debug=True)