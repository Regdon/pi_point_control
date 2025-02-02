class Node:
    def __init__(self, id, x, y, parent):
        self.id = id
        self.x = x
        self.y = y
        self.parent = parent
        self.state = "None"
        self.order = 0

    def Setup(self, node_list):
        #undefined for standard node
        pass

    def __str__(self):
        return self.id
    
    def valid_parent(self):
        return isinstance(self.parent, Node)

    def to_dict(self):
        if self.valid_parent():
            return {"x1": self.x, "y1": self.y, 'x2': self.parent.x, "y2": self.parent.y,"state": self.state}
        else:
            return {"error": "Node ID " + self.id + " missing Parent Node"}
        
    def CalculateState(self):
        self.state = self.parent.GetState(self.id)

    def GetState(self, child_id):
        return self.state
    
    def GetParent(self):
        return self.parent
    
    def GetChild(self):
        #undefined for a standard node
        return 0