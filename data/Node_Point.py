from .Node import Node

class Node_Point(Node):
    def __init__(self, id, x, y, parent, child_id_1, child_id_2, node, point):
        Node.__init__(self, id, x, y, parent)

        self.children = ["", child_id_1, child_id_2]
        self.point_state = 1
        self.node = node
        self.point = point

    def SetPointState(self, val):
        self.point_state = val

    def GetState(self, child_id):
        if (child_id == self.children[self.point_state]):
            return self.state
        else:
            return "#000000"
        
    def switch(self):
        if (self.point_state == 1):
            self.point_state = 2
        else:
            self.point_state = 1