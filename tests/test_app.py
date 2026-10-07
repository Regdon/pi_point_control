import contextlib
import io
import json
import os
import tempfile
import unittest

from Point_Engine import Point_Engine
from server import create_app
import static


class ApplicationFactoryTests(unittest.TestCase):
    def test_point_state_changes_send_i2c_state(self):
        class I2CRecorder:
            def __init__(self):
                self.states = []

            def SendState(self, node, point, state):
                self.states.append((node, point, state))

        i2c = I2CRecorder()
        engine = Point_Engine(i2c=i2c)
        engine.LoadData()
        point = next(
            point for point in engine.node_list
            if point.id == "york_facing_crossover_point_outer"
        )

        point.TogglePointState()
        point.SetPointState(1)
        point.SetPointState(1)

        self.assertEqual(i2c.states, [(1, 3, 1), (1, 3, 0)])

    def test_route_state_changes_send_i2c_state(self):
        class I2CRecorder:
            def __init__(self):
                self.states = []

            def SendState(self, node, point, state):
                self.states.append((node, point, state))

        i2c = I2CRecorder()
        engine = Point_Engine(i2c=i2c)
        engine.LoadData()
        engine.LoadRoutes()
        engine.SetupRoutes()

        route = engine.route_list[0]
        changed_route_point = next(
            route_point
            for route_point in route.route.values()
            if route_point["node"].point_state != route_point["state"]
        )
        point = changed_route_point["node"]
        route.HandleClick(route.button_centre_x, route.button_centre_y)

        self.assertEqual(
            i2c.states,
            [(
                point.node,
                point.point,
                point.point_state - static.POINT_STATE_STRAIGHT,
            )],
        )
        self.assertEqual(point.point_state, changed_route_point["state"])

    def test_point_address_values_are_retained_by_point_models(self):
        engine = Point_Engine()
        engine.LoadData()

        points = {point.id: point for point in engine.node_list if hasattr(point, "point")}
        self.assertEqual(
            (points["york_facing_crossover_point_outer"].node,
             points["york_facing_crossover_point_outer"].point),
            (1, 3),
        )
        self.assertEqual(
            (points["york_facing_crossover_point_inner"].node,
             points["york_facing_crossover_point_inner"].point),
            (1, 4),
        )

    def test_app_loads_configuration_outside_project_directory(self):
        original_directory = os.getcwd()
        with tempfile.TemporaryDirectory() as working_directory:
            try:
                os.chdir(working_directory)
                with contextlib.redirect_stdout(io.StringIO()):
                    app = create_app()
                    response = app.test_client().get("/")
                    socketio = app.extensions["socketio"]
                    client = socketio.test_client(app)
                    events = client.get_received()
                    client.disconnect()
            finally:
                os.chdir(original_directory)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([event["name"] for event in events], ["update"])
        payload = events[0]["args"]
        if len(payload) == 1 and isinstance(payload[0], str):
            payload = json.loads(payload[0])
        self.assertIsInstance(payload, list)


if __name__ == "__main__":
    unittest.main()
