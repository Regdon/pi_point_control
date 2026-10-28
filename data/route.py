import static
from .Node_Point import Node_Point

class Route:
    def __init__(self, data):
        self.id = data["id"]
        self.button_centre_x = int(data["button_centre_x"])
        self.button_centre_y = int(data["button_centre_y"])
        self.button_height = int(data["button_height"])
        self.button_width = int(data["button_width"])
        self.button_colour_scheme = data["button_colour_scheme"]
        self.point_list = {
            point["id"]: point["state"]
            for point in data["points"]
        }
        self.route = {}
        self.route_set = 0
        self.state = 0

    def SetupRoute(self, node_list):
        self.route = {}
        all_nodes_found = True

        for node_id, state in self.point_list.items():
            if state == "Straight":
                state = static.POINT_STATE_STRAIGHT
            elif state == "Turnout":
                state = static.POINT_STATE_TURNOUT

            for node in node_list:
                if node.id == node_id:
                    self.route[node_id] = {
                        "node": node,
                        "state": state
                    }
                    break
            else:
                all_nodes_found = False

        return 1 if all_nodes_found else 0

    def HandleClick(self, gridX, gridY):
        half_width = self.button_width / 2
        half_height = self.button_height / 2

        if (abs(gridX - self.button_centre_x) > half_width or
                abs(gridY - self.button_centre_y) > half_height):
            return 0

        state = self.CalculateState()

        if state == 0:
            for route_point in self.route.values():
                if isinstance(route_point["node"], Node_Point):
                    route_point["node"].LockToState(route_point["state"])
            self.route_set = 1
        elif state == 1:
            for route_point in self.route.values():
                if isinstance(route_point["node"], Node_Point):
                    route_point["node"].ClearLockedState()
            self.route_set = 0

        return 1

    def CalculateState(self):
        if self.route_set == 1:
            self.state = 1
            return self.state

        for route_point in self.route.values():
            if (isinstance(route_point["node"], Node_Point) and
                    route_point["node"].locked == 1):
                self.state = 2
                return self.state

        self.state = 0
        return self.state

    def GetDrawScript(self):
        self.CalculateState()
        colour_scheme = static.ROUTE_COLOUR_SCHEMES.get(self.button_colour_scheme, {})
        x_inset = static.GRID_SIZE_X * 0.1
        y_inset = static.GRID_SIZE_Y * 0.1

        return {
            "type": "route_button",
            "x1": (self.button_centre_x - self.button_width / 2) * static.GRID_SIZE_X + x_inset,
            "y1": (self.button_centre_y - self.button_height / 2) * static.GRID_SIZE_Y + y_inset,
            "width": self.button_width * static.GRID_SIZE_X - 2 * x_inset,
            "height": self.button_height * static.GRID_SIZE_Y - 2 * y_inset,
            "colour": colour_scheme.get(self.state, self.button_colour_scheme)
        }
