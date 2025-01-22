from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from Point_Engine import Point_Engine

if __name__ == '__main__':
    engine = Point_Engine()

    engine.LoadData()
    engine.CalculateOrder()
    engine.CalculateState()

    app = Flask(__name__)
    socketio = SocketIO(app)

    socketio.run(app, debug=True)

@app.route('/')
def index():
    data = {'message': 'Hello, World!'}
    return render_template('index.html', data=data)

@socketio.on('connect')
def handle_connect():
    emit('update', engine.GetWebJSON())

