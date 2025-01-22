from data.Node import Node
from data.Node_Source import Node_Source

import json

class Point_Engine:
    def __init__(self):
        self.nodeList = []

    def GetNodeByID(self, id):
        for node in self.nodeList:
            if (node.id == id):
                return node
            
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
