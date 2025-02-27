import static

class Node:
    def __init__(self, id, x, y, parent):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.parent = parent
        self.state = "None"
        self.order = 0
        self.route_set = ""

    def Setup(self, node_list):
        #undefined for standard node
        pass

    def __str__(self):
        return self.id
    
    def valid_parent(self):
        return isinstance(self.parent, Node)

    def append_to_dict(self, dict):
        if self.valid_parent():
            dict.append({"x1": self.GetGridX(), "y1": self.GetGridY(), 'x2': self.parent.GetGridX(), "y2": self.parent.GetGridY(),"state": self.state})
        else:
            dict.append({"error": "Node ID " + self.id + " missing Parent Node"})
        
    def CalculateState(self):
        self.state = self.parent.GetState(self.id)

    def GetState(self, child_id):
        return self.state
    
    def GetParent(self):
        return self.parent
    
    def GetChild(self):
        #undefined for a standard node
        return 0
    
    def GetParentOrder(self):
        return self.parent.order
    
    def GetGridX(self):
        return self.x * static.GRID_SIZE_X
    
    def GetGridY(self):
        return self.y * static.GRID_SIZE_Y
    
    def IsRouteSet(self):
        if (self.route_set):
            return 1
        else:
            return 0
        
    def SetByRoute(self, route_id, state):
        self.route_set = route_id
        self.state = state

    def ClearByRoute(self):
        self.route_set = ""