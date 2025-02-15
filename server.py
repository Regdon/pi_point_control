from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from Point_Engine import Point_Engine

import static

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    data = {'message': 'Hello, World!'}
    return render_template('index.html', data=data)

@socketio.on('connect')
def handle_connect():
    print(engine.GetWebJSON())
    emit('update', engine.GetWebJSON())

@socketio.on('click')
def handle_click(data):
    print("click")
    gridX = int(data['x']) / static.GRID_SIZE_X
    gridY = int(data['y']) / static.GRID_SIZE_Y
    isChange = engine.HandleClick(gridX, gridY)
    print(f"X={data['x']}, Y={data['y']}, GridX={gridX}, GridY={gridY}")
    if (isChange == 1):
        engine.CalculateState()
        emit('update', engine.GetWebJSON())

if __name__ == '__main__':
    engine = Point_Engine()

    engine.LoadData()
    engine.Setup()
    engine.CalculateOrder()
    engine.CalculateState()

    socketio.run(app, host='0.0.0.0', port=5000)



