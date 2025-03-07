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
        self.colour_locked = data["colour_locked"]
        self.colour_set = data["colour_set"]

        self.route = []
        self.routeStates = []

        self.route_set = 0

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

    def CheckBlocked(self):
        #print("Check Blocked Function")

        if (self.route_set == static.ROUTE_STATE_ACTIVE):
            return self.route_set
        
        for route_state in self.routeStates:
            if (not route_state.can_set()):
                self.route_set = static.ROUTE_STATE_BLOCKED
                return self.route_set

        self.route_set = static.ROUTE_STATE_DEFAULT
        return self.route_set

    def SetRoute(self):
        #print("Set Route Function")
        for route_state in self.routeStates:
            if (not route_state.can_set()):
                print("Route Locked")
                return
        
        for route_state in self.routeStates:
            route_state.set()

        self.route_set = static.ROUTE_STATE_ACTIVE
  
    def ClearRoute(self):
        #print("Clear Route Function")
        for route_state in self.routeStates:
            route_state.clear()

        self.route_set = static.ROUTE_STATE_DEFAULT

    def toggle(self):
        #print("Route Toggle Function")
        if (self.route_set == static.ROUTE_STATE_DEFAULT):
            self.SetRoute()
        else:
            self.ClearRoute()

    def append_to_dict(self, dict):
        dict.append({
            "type": "route_button"
            ,"x1": self.position_x * static.GRID_SIZE_X
            ,"y1": self.position_y * static.GRID_SIZE_Y
            ,"width": 4 * static.GRID_SIZE_X
            ,"height": 2 * static.GRID_SIZE_Y
            ,"colour": self.getColour()
            ,"active": self.route_set
        })

    def position_in_button(self, x, y):
        return (x >= self.position_x and y >= self.position_y and x <= self.position_x + 4 and y <= self.position_y + 2)
    
    def getColour(self):
        if (self.route_set == static.ROUTE_STATE_ACTIVE):
            return self.colour_set
        elif (self.route_set == static.ROUTE_STATE_BLOCKED):
            return self.colour_locked
        else:
            return self.colour
        
           
class RouteState:
    def __init__(self, node, state):
        self.node = node
        self.state = state

    def can_set(self):
        #print("Route State Can Set Function")
        return not self.node.IsRouteSet()

    def set(self):
        #print("Route State Set Function")
        if (self.can_set()):
            self.node.SetByRoute("temp", self.state)

    def clear(self):
        #print("Route State Clear Function")
        self.node.ClearByRoute()
