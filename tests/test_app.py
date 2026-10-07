import contextlib
import io
import json
import os
import tempfile
import unittest

from Point_Engine import Point_Engine
from server import create_app


class ApplicationFactoryTests(unittest.TestCase):
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
