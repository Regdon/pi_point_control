from .Node_Point import Node_Point

import static

class RouteButton:
    """
    Represents a clickable button on the GUI which defines a route between two notes.
    The button has three states, one for the route being settable, one for it being blocked and one for it being clearable    
    """
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

        self.routes = []

        self.route_set = 0

    def SetupRoute(self, engine):
        """
        Function to calculate a list of possible routes between the start and end point and store them in routes[], a list of 1 or more RouteOption
        """
        debug = True
        if (debug):
            print("------------------------------------------")
            print(f"Running SetupRoute for Route ID {self.id}")
            print(f"Node ID Start: {self.node_id_start}, Node ID End: {self.node_id_end}")   
 
        #Get a list of possible routes. A route is a list of nodes, making this a list of a list of nodes
        list_routes = engine.GetRoute(self.node_id_start, self.node_id_end)

        if (debug):
            row = 0
            for route in list_routes:
                str = ""
                for node in route:
                    str = str + node.id + "-->"
                print(f"Route {row}: {str}")
                row = row + 1          

        #Loop through routes, and create a route option for each.
        #A route option stores a single possible route
        for individual_route in list_routes:
            route = RouteOption(individual_route)
            self.routes.append(route)

    def CalculateButtonState(self):
        """
        This funtion calculates if the the route is settable, blocked or clearable.
        Returns the state.
        """

        if (self.id == "Leeds D to York Platform"):
            pass

        #First, are any of the possible routes set, if so the route is active / clearable
        for route in self.routes:
            if (route.isSet()):
                self.route_set = static.ROUTE_STATE_ACTIVE
                return self.route_set
        
        #Second, if the route isn't set, can any of the routes be set
        countBlocked = 0
        for route in self.routes:
            if (route.isBlocked()):
                countBlocked += 1
        if (countBlocked == len(self.routes)):
            self.route_set = static.ROUTE_STATE_BLOCKED
            return self.route_set  


        #Third, if no other condtion applies, then the route is settable
        self.route_set = static.ROUTE_STATE_DEFAULT
        return self.route_set

    def GetButtonState(self):
        """
        This function returns the current state of the button, either settable, blocked or clearable
        """
        return self.route_set

    def SetRoute(self):
        """
        This function sets the route, which will prevent any other routes using those points (blocked) until cleared
        """
        debug = True
        if debug:
            print("------------------")
            print("RouteButton Level: Set Route Function")

        #We have to loop through possible routes to find one which is settable
        for route in self.routes:
            if (not route.isBlocked()):
                route.SetRoute()
                return True
            
        #If returning false, then something has gone wrong because none of the routes could be set
        return False

    def ClearRoute(self):
        """
        This function clears the route, which will allow other routes to use any previously blocked points
        """
        #We have to loop through possible routes to find which one is currently set
        for route in self.routes:
            if (route.isSet()):
                route.ClearRoute()
                return True
        
        #If returning false, then something has gone wrong because none of the routes are currently set
        return False

    def append_to_dict(self, dict):
        """
        This function writes the button data into JSON format to send to the web browser
        """
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
        """
        This function detects if a click was within the button
        """
        return (x >= self.position_x and y >= self.position_y and x <= self.position_x + 4 and y <= self.position_y + 2)
    
    def getColour(self):
        """
        This functions returns the colour of the button based on the current set state
        """
        if (self.route_set == static.ROUTE_STATE_ACTIVE):
            return self.colour_set
        elif (self.route_set == static.ROUTE_STATE_BLOCKED):
            return self.colour_locked
        else:
            return self.colour



class RouteOption:
    def __init__(self, data):
        self.route = data
        self.routeStates = []
        self.route_set = 0

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

    def isSet(self):
        """
        This function returns True or False is the route currently set.
        """
        return self.route_set

    def isBlocked(self):
        """
        This functions returns True of False is the route currently blocked.
        """
        for routeState in self.routeStates:
            if (routeState.isBlocked()):
                return True
            
        return False

    def SetRoute(self):
        """
        This function sets the route
        """
        debug = True
        if debug:
            print("------------------")
            print("RouteOption Level: Set Route Function")
            print(f"route: {self.PrintRoute()}")

        for routeState in self.routeStates:
            routeState.SetRoute()

        self.route_set = True

    def ClearRoute(self):
        """
        This function clears the route
        """
        for routeState in self.routeStates:
            routeState.ClearRoute()

        self.route_set = False

    def NodeInRoute(self, node_id):
        """
        This function checks if a given node is part of this route
        """
        for node in self.route:
            if (node.id == node_id):
                return True
        return False
    
    def PrintRoute(self):
        str = ""
        for node in self.route:
            str = str + node.id + " --> "
        return str

class RouteState:
    def __init__(self, node, state):
        self.node = node
        self.state = state

    def isBlocked(self):
        return self.node.IsRouteSet(self.state)

    def SetRoute(self):
        """
        This function sets the routes
        """
        debug = True
        if debug:
            print("------------------")
            print("RouteState Level: Set Route Function")
            print(f"Node: {self.node.id}, route setting to {self.state}")
        self.node.SetByRoute("temp", self.state)

    def ClearRoute(self):
        """
        This function clears the set route
        """
        self.node.ClearByRoute()