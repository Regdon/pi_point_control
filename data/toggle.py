import static
from .Node_Point import Node_Point


class Toggle:
    def __init__(self, data):
        self.id = data["id"]
        self.button_centre_x = int(data["button_centre_x"])
        self.button_centre_y = int(data["button_centre_y"])
        self.button_height = int(data["button_height"])
        self.button_width = int(data["button_width"])
        self.button_colour_scheme = data["button_colour_scheme"]
        self.default_state = (
            static.POINT_STATE_STRAIGHT
            if data["default_state"] == "Straight"
            else static.POINT_STATE_TURNOUT
        )
        self.point_ids = [point["id"] for point in data["points"]]
        self.route_colours = {
            route["id"]: route["colour"] for route in data["routes"]
        }
        self.node_colours = {
            node["id"]: node["colour"] for node in data["nodes"]
        }
        self.points = []
        self.routes = {}
        self.nodes = {}
        self.is_on = False

    def Setup(self, node_list, route_list):
        nodes_by_id = {node.id: node for node in node_list}
        routes_by_id = {route.id: route for route in route_list}
        self.points = [nodes_by_id[node_id] for node_id in self.point_ids]
        self.routes = {
            route_id: routes_by_id[route_id]
            for route_id in self.route_colours
        }
        self.nodes = {
            node_id: nodes_by_id[node_id]
            for node_id in self.node_colours
        }
        self._apply_point_state()
        self._apply_node_colours()
        return 1

    def _apply_point_state(self):
        if self.is_on:
            point_state = (
                static.POINT_STATE_STRAIGHT
                if self.default_state == static.POINT_STATE_TURNOUT
                else static.POINT_STATE_TURNOUT
            )
        else:
            point_state = self.default_state

        for point in self.points:
            if not isinstance(point, Node_Point):
                raise TypeError(f"Toggle {self.id!r} references a non-point node")
            point.ClearLockedState()
            point.LockToState(point_state)

    def HandleClick(self, grid_x, grid_y):
        half_width = self.button_width / 2
        half_height = self.button_height / 2
        if (
            abs(grid_x - self.button_centre_x) > half_width
            or abs(grid_y - self.button_centre_y) > half_height
        ):
            return 0

        self.is_on = not self.is_on
        self._apply_point_state()
        self._apply_node_colours()
        return 1

    def _apply_node_colours(self):
        for node_id, node in self.nodes.items():
            if self.is_on:
                node.SetDrawColourOverride(self.id, self.node_colours[node_id])
            else:
                node.ClearDrawColourOverride(self.id)

    def GetDrawScript(self):
        half_width = self.button_width / 2
        half_height = self.button_height / 2
        x_inset = static.GRID_SIZE_X * 0.1
        y_inset = static.GRID_SIZE_Y * 0.1
        colour_state = (
            static.ROUTE_STATE_ACTIVE if self.is_on else static.ROUTE_STATE_DEFAULT
        )
        colour_scheme = static.ROUTE_COLOUR_SCHEMES[self.button_colour_scheme]
        return {
            "type": "toggle_button",
            "x1": (self.button_centre_x - half_width) * static.GRID_SIZE_X + x_inset,
            "y1": (self.button_centre_y - half_height) * static.GRID_SIZE_Y + y_inset,
            "width": self.button_width * static.GRID_SIZE_X - 2 * x_inset,
            "height": self.button_height * static.GRID_SIZE_Y - 2 * y_inset,
            "colour": colour_scheme[colour_state],
        }
