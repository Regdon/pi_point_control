from .Node import Node

class Node_Source(Node):
    def __init__(self, id, x, y, colour):
        Node.__init__(self, id, x, y, "")
        self.colour = colour
        self.order = 1

    def CalculateState(self):
        self.state = self.colour