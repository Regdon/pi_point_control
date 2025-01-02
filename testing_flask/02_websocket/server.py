from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('button_pressed')
def handle_button_press():
    print('Button was pressed')
    emit('response', 'Button was pressed!')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
