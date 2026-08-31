import static

class Node:
    def __init__(self, id, x, y, parent_id):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.parent_id = parent_id
        self.draw_colour = None

    def SetupParent(self, node_list):
        for node in node_list:
            if node.id == self.parent_id:
                self.parent = node
                return 1
        else:
            self.parent = None
            return 0
        
    def CalculateDrawColour(self):
        if self.parent is not None:
            self.draw_colour = self.parent.GetDrawColour(self.id)

    def GetDrawColour(self, child_node_id):
        return self.draw_colour

    def GetGridX(self):
        return self.x * static.GRID_SIZE_X
    
    def GetGridY(self):
        return self.y * static.GRID_SIZE_Y  

    def GetDrawScript(self):
        if self.parent is not None:
            return {"x1": self.GetGridX(), "y1": self.GetGridY(), 'x2': self.parent.GetGridX(), "y2": self.parent.GetGridY(),"colour": self.draw_colour}
        else:
            return {"error": "Node ID " + self.id + " missing Parent Node"}