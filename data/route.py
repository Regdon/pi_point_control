from .Node_Point import Node_Point

import static

class Route:
    def __init__(self, data):
        self.id = data["id"]
        self.node_id_start = data["node_id_start"]
        self.node_id_end = data["node_id_end"]
        self.position_x = int(data["position_x"])
        self.position_y = int(data["position_y"])
        self.align = data["align"]
        self.colour = data["colour"]

        self.route = []
        self.routeStates = []

    def SetupRoute(self, engine):
        self.route = engine.GetRoute(self.node_id_start, self.node_id_end)

        s = f"route from {self.node_id_start} to {self.node_id_end}:"
        for node in self.route:
            s += f"{node.id}, "
        print(s)
    
        for node in self.route:
            if isinstance(node, Node_Point):
                if self.NodeInRoute(node.set_straight_id):
                    obj = RouteState(node, static.POINT_STATE_STRAIGHT)
                    self.routeStates.append(obj)
                    print(f"Node ID {node.id} must be set straight for this route")
                elif self.NodeInRoute(node.set_turnout_id):
                    obj = RouteState(node, static.POINT_STATS_TURNOUT)
                    self.routeStates.append(obj)
                    print(f"Node ID {node.id} must be set turnout for this route")

    def NodeInRoute(self, node_id):
        for node in self.route:
            if (node.id == node_id):
                return True
        return False

    def SetRoute(self):
        print("Set Route Function")
        pass

    def ClearRoute(self):
        print("Clear Route Function")
        pass

    def append_to_dict(self, dict):
        dict.append({
            "type": "route_button"
            ,"x1": self.position_x * static.GRID_SIZE_X
            ,"y1": self.position_y * static.GRID_SIZE_Y
            ,"width": 2 * static.GRID_SIZE_X
            ,"height": 1 * static.GRID_SIZE_Y
            ,"colour": self.colour
            ,"active": 0
        })

    def position_in_button(self, x, y):
        return (x >= self.position_x and y >= self.position_y and x <= self.position_x + (2 * static.GRID_SIZE_X) and y <= self.position_y + static.GRID_SIZE_Y)

class RouteState:
    def __init__(self, node, state):
        self.node = node
        self.state = state
