from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    data = {'message': 'Hello, World!'}
    return render_template('index.html', data=data)

@socketio.on('connect')
def handle_connect():
    emit('update', {"points":[{"name":"test", "state":"0", "type":"point", "position":[{"type":"common", "x":"100", "y":"100"}, {"type":"end-a", "x":"200", "y":"100"}, {"type":"end-b", "x":"200", "y":"200"}]}]})

if __name__ == '__main__':
    socketio.run(app, debug=True)


