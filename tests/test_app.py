import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest.mock import Mock

from Point_Engine import Point_Engine
from server import create_app
import static
from i2c import i2c_control


class ApplicationFactoryTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows-only I2C simulation")
    def test_i2c_control_runs_without_hardware_on_windows(self):
        with self.assertLogs("i2c", level="WARNING") as logs:
            control = i2c_control()

        self.assertIsNone(control.bus)
        self.assertIn("point changes will be local only", logs.output[0])
        control.SendState(1, 3, 1)

    def test_i2c_control_sends_state_using_injected_bus(self):
        bus = Mock()
        control = i2c_control(bus=bus)
        control.SendState(1, 3, 1)

        bus.write_i2c_block_data.assert_called_once_with(16, 0, [83])

    def test_point_state_changes_send_i2c_state(self):
        class I2CRecorder:
            def __init__(self):
                self.states = []

            def SendState(self, node, point, state):
                self.states.append((node, point, state))

        i2c = I2CRecorder()
        engine = Point_Engine(i2c=i2c)
        engine.LoadData()
        i2c.states.clear()
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
        i2c.states.clear()
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

    def test_load_data_sends_each_point_default_state(self):
        class I2CRecorder:
            def __init__(self):
                self.states = []

            def SendState(self, node, point, state):
                self.states.append((node, point, state))

        i2c = I2CRecorder()
        engine = Point_Engine(i2c=i2c)
        engine.LoadData()
        points = [
            point for point in engine.node_list
            if hasattr(point, "point_default_state")
        ]
        expected_states = [
            (
                point.node,
                point.point,
                point.point_state - static.POINT_STATE_STRAIGHT,
            )
            for point in points
        ]

        self.assertEqual(i2c.states, expected_states)
        self.assertEqual(len(i2c.states), len(points))

    def test_reset_points_refuses_to_change_route_locked_points(self):
        i2c = Mock()
        engine = Point_Engine(i2c=i2c)
        engine.LoadData()
        engine.LoadRoutes()
        engine.SetupRoutes()
        point = next(
            point for point in engine.node_list
            if point.id == "york_siding_a_b"
        )
        point.SetPointState(static.POINT_STATE_STRAIGHT)
        point.LockToState(static.POINT_STATE_TURNOUT)
        i2c.SendState.reset_mock()

        success, locked_point_ids = engine.ResetPointsToDefault()

        self.assertFalse(success)
        self.assertIn(point.id, locked_point_ids)
        self.assertEqual(point.point_state, static.POINT_STATE_TURNOUT)
        i2c.SendState.assert_not_called()

    def test_reset_points_restores_defaults_and_sends_changed_states(self):
        i2c = Mock()
        engine = Point_Engine(i2c=i2c)
        engine.LoadData()
        points = [
            point for point in engine.node_list
            if hasattr(point, "point_default_state")
        ]
        point = next(
            point for point in points
            if point.point_default_state == static.POINT_STATE_STRAIGHT
        )
        point.SetPointState(static.POINT_STATE_TURNOUT)
        i2c.SendState.reset_mock()

        success, locked_point_ids = engine.ResetPointsToDefault()

        self.assertTrue(success)
        self.assertEqual(locked_point_ids, [])
        self.assertEqual(point.point_state, point.point_default_state)
        i2c.SendState.assert_called_once_with(
            point.node,
            point.point,
            0,
        )

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
                    client.emit("reset_points")
                    reset_events = client.get_received()
                    client.disconnect()
            finally:
                os.chdir(original_directory)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([event["name"] for event in events], ["update"])
        payload = events[0]["args"]
        if len(payload) == 1 and isinstance(payload[0], str):
            payload = json.loads(payload[0])
        self.assertIsInstance(payload, list)
        self.assertEqual(
            [event["name"] for event in reset_events],
            ["update", "reset_result"],
        )
        self.assertEqual(
            reset_events[1]["args"][0],
            {"success": True, "locked_points": []},
        )


if __name__ == "__main__":
    unittest.main()
