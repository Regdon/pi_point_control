from .Node import Node
from i2c import i2c_control

import static

class Node_Point(Node):
    def __init__(self, id, x, y, point_type, single_end_id, set_straight_id, set_turnout_id, node, point, i2c):
        Node.__init__(self, id, x, y, "")

        self.point_type = point_type
        self.single_end_id = single_end_id
        self.set_straight_id = set_straight_id
        self.set_turnout_id = set_turnout_id
        
        self.single_end = ""
        self.set_straight = ""
        self.set_turnout = ""

        self.point_state = 1
        self.node = node
        self.point = point

        self.route_set = ""

        self.i2c = i2c

    def Setup(self, node_list):
        for node in node_list:
            if (node.id == self.single_end_id):
                self.single_end = node
            elif (node.id == self.set_straight_id):
                self.set_straight = node
            elif (node.id == self.set_turnout_id):
                self.set_turnout = node            

    def SetPointState(self, val):
        self.point_state = val

    def CalculateState(self):
        self.state = self.GetParent().GetState(self.id)

    def GetState(self, child_id):
        if (child_id == self.GetChild().id):
            return self.state
        else:
            return "#000000"
        
    def switch(self):
        if (self.point_state == 1):
            self.point_state = 2
        else:
            self.point_state = 1
        self.i2c.SendState(self.node, self.point, self.point_state - 1)

    def GetParent(self):
        if (self.point_type == static.POINT_TYPE_CONVERGE):
            #Two parents, so check which way the points face
            if self.point_state == 1:
                return self.set_straight
            elif self.point_state == 2:
                return self.set_turnout
            else:
                return 0
        elif (self.point_type == static.POINT_TYPE_DIVERGE):
            #One parent
            return self.single_end
        else:
            #Error
            return 0

    def GetChild(self):
        if (self.point_type == static.POINT_TYPE_CONVERGE):
            #One Child
            return self.single_end
        elif (self.point_type == static.POINT_TYPE_DIVERGE):
            #Two Children, so check which way the points face
            if self.point_state == 1:
                return self.set_straight
            elif self.point_state == 2:
                return self.set_turnout
            else:
                return 0
        else:
            #Error
            return 0
        
    def GetParentOrder(self):
        if (self.point_type == static.POINT_TYPE_CONVERGE):
            p1 = self.set_straight.order
            p2 = self.set_turnout.order
            return min(p1, p2)
        elif (self.point_type == static.POINT_TYPE_DIVERGE):
            return self.single_end.order
        else:
            return 0
        
    def append_to_dict(self, dict):
        if (self.point_type == static.POINT_TYPE_CONVERGE):
            dict.append({"x1": self.GetGridX(), "y1": self.GetGridY(), 'x2': self.set_straight.GetGridX(), "y2": self.set_straight.GetGridY(),"state": self.set_straight.state})
            dict.append({"x1": self.GetGridX(), "y1": self.GetGridY(), 'x2': self.set_turnout.GetGridX(), "y2": self.set_turnout.GetGridY(),"state": self.set_turnout.state})
        elif (self.point_type == static.POINT_TYPE_DIVERGE):
            dict.append({"x1": self.GetGridX(), "y1": self.GetGridY(), 'x2': self.single_end.GetGridX(), "y2": self.single_end.GetGridY(),"state": self.state})

    def IsRouteSet(self):
        if (self.route_set == ""):
            print(f"Checking if {self.id} is locked. Clear")
            return 0
        else:
            print(f"Checking if {self.id} is locked. Locked")
            return 1
        
    def SetByRoute(self, route_id, state):
                    
        self.route_set = route_id
        if (self.point_state != state):
            self.point_state = state
            print(f"Node {self.id} routed to {state}.")
            self.i2c.SendState(self.node, self.point, self.point_state - 1)
        else:
            print(f"Node {self.id} routed, but state unchanged")

    def ClearByRoute(self):
        self.route_set = ""
        print(f"Node {self.id} route cleared")