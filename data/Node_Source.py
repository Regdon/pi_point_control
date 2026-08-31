from .Node import Node

class Node_Source(Node):
    def __init__(self, id, x, y, colour):
        Node.__init__(self, id, x, y, "")
        self.colour = colour
        self.draw_colour = colour

    def SetupParent(self, node_list):
        self.parent = None
        return 0
    
    def CalculateDrawColour(self):
        self.draw_colour = self.colour

    def GetDrawScript(self):
        return None