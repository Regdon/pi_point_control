from .Node import Node

import static

class Node_Point(Node):
    def __init__(self, id, x, y, point_type, single_end_id, set_straight_id, set_turnout_id, node, point):
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