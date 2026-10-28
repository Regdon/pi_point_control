from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from Point_Engine import Point_Engine

import static


def create_app() -> Flask:
    app = Flask(__name__)
    socketio = SocketIO(app)
    engine = Point_Engine()
    engine.LoadData()
    engine.SetupAllNodeParents()
    engine.CalculateAllNodeDrawColours()
    engine.LoadRoutes()
    engine.SetupRoutes()

    @app.route('/')
    def home():
        data = {'message': 'Hello, World!'}
        return render_template('index.html', data=data)

    @socketio.on('connect')
    def handle_connect():
        print(engine.GetAllDrawScripts())
        emit('update', engine.GetAllDrawScripts())

    @socketio.on('click')
    def handle_click(data):
        print("click")
        gridX = int(data['x']) / static.GRID_SIZE_X
        gridY = int(data['y']) / static.GRID_SIZE_Y
        isChange = engine.HandleClick(gridX, gridY)
        print(f"X={data['x']}, Y={data['y']}, GridX={gridX}, GridY={gridY}")
        if isChange == 1:
            engine.CalculateAllNodeDrawColours()
            engine.CalculateAllRouteStates()
            emit('update', engine.GetAllDrawScripts())

    @socketio.on('reset_points')
    def handle_reset_points():
        success, locked_point_ids = engine.ResetPointsToDefault()
        if success:
            engine.CalculateAllNodeDrawColours()
            engine.CalculateAllRouteStates()
            emit('update', engine.GetAllDrawScripts())

        emit(
            'reset_result',
            {
                'success': success,
                'locked_points': locked_point_ids,
            },
        )

    return app


if __name__ == '__main__':
    app = create_app()
    socketio = app.extensions['socketio']
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
