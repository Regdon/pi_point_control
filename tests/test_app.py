import contextlib
import io
import json
import os
import tempfile
import unittest

from server import create_app


class ApplicationFactoryTests(unittest.TestCase):
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
