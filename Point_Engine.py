from data.Node import Node
from data.Node_Source import Node_Source
from data.Node_Point import Node_Point

import json

from i2c import i2c_control

class Point_Engine:
    def __init__(self):
        self.nodeList = []
        self.i2c = i2c_control()

    def GetNodeByID(self, id):
        for node in self.nodeList:
            if (node.id == id):
                return node
            
    def Setup(self):
        for node in self.nodeList:
            node.Setup()

    def CalculateOrder(self):
        #Type Node_Source defaults to order 1 at initilisation
        #Now need to loop through other objects to find correct ordering
        changes = 1
        while changes == 1:
            changes = 0
            for node in self.nodeList:
                if node.order == 0:
                    if node.parent.order != 0:
                        node.order = node.parent.order + 1
                        changes = 1

    def ResetState(self):
        for node in self.nodeList:
            node.state = "None"

    def CalculateState(self):
        self.ResetState()

        for node in self.nodeList:
            node.CalculateState()

    def GetWebJSON(self):
        dict = []
        for node in self.nodeList:
            if isinstance(node, Node_Source):
                continue
            else:
                dict.append(node.to_dict())

        return json.dumps(dict)

    def LoadData(self):
        with open('data/data.json', 'r') as file:
            data = json.load(file)

        for node in data["nodes"]:
            if (node["type"] == "node"):
                obj = Node(node["id"], node["x"], node["y"], self.GetNodeByID(node["parent"]))
                self.nodeList.append(obj)

            if (node["type"] == "node-source"):
                obj = Node_Source(node["id"], node["x"], node["y"], node["colour"])
                self.nodeList.append(obj)
            
            if (node["type"] == "node-point"):
                obj = Node_Point(node["id"], node["x"], node["y"], node["point_type"], node["single_end_id"], node["set_straight_id"], node["set_turnout_id"], node["node"], node["point"])
                self.nodeList.append(obj)

    def HandleClick(self, x, y):
        for node in self.nodeList:
            if isinstance(node, Node_Point):
                abs_dif_x = abs(x - int(node.x))
                abs_dif_y = abs(y - int(node.y))

                if (abs_dif_x < 25 and abs_dif_y < 25):
                    print(node.id + ' clicked')
                    node.switch()
                    self.i2c.SendState(node.node, node.point, node.point_state - 1)
                    return 1
        return 0


#Sorting list by order::
# # Sample dictionary with nested objects
# my_dict = {
#     'item1': {'name': 'banana', 'order': 3},
#     'item2': {'name': 'apple', 'order': 2},
#     'item3': {'name': 'cherry', 'order': 5}
# }

# # Sort the dictionary by the 'order' property of nested objects
# ordered_dict = dict(sorted(my_dict.items(), key=lambda item: item[1]['order']))

# print(ordered_dict)
