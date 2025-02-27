from data.Node import Node
from data.Node_Source import Node_Source
from data.Node_Point import Node_Point
from data.route import Route

import json
import static

from i2c import i2c_control

class Point_Engine:
    def __init__(self):
        self.nodeList = []
        self.routeList = []
        self.i2c = i2c_control()

    def GetNodeByID(self, id):
        for node in self.nodeList:
            if (node.id == id):
                return node
            
    def GetRoute(self, id_from, id_to):
        result = []

        node_current = self.GetNodeByID(id_from)
        # print(f"Starting routing for {node_current}")

        while True:            
            if (node_current.id == id_to):
                # print(f"Target node {node_current} found, stopping")
                result.append(node_current) 
                return result
            elif isinstance(node_current, Node_Source):
                #If we get here, no route has been found, return 0
                # print(f"Source node {node_current} found, unable to find target")
                return 0
            elif isinstance(node_current, Node_Point):
                if (node_current.point_type == static.POINT_TYPE_CONVERGE):
                    #This is the tricky siutation, because we don't know which way to go to our destination. 
                    route_straight = self.GetRoute(node_current.set_straight_id, id_to)
                    route_turnout = self.GetRoute(node_current.set_turnout_id, id_to)
                    if (route_straight):
                        # print(f"Following straight from point {node_current}")
                        result.append(node_current)
                        for part in route_straight:
                            result.append(part)
                        return result
                    elif (route_turnout):
                        # print(f"Following turnout from point {node_current}")
                        result.append(node_current)
                        for part in route_turnout:
                            result.append(part)
                        return result
                    else:
                        # print(f"Routing error from point {node_current}, this shouldn't happen")
                        return 0
                else:
                    # print(f"Divering point {node_current} found, continuing to parent")
                    result.append(node_current)
                    node_current = node_current.GetParent()                
            else:
                # print(f"node {node_current} found, continuing to parent")
                result.append(node_current)
                node_current = node_current.GetParent()
            
    def Setup(self):
        for node in self.nodeList:
            node.Setup(self.nodeList)

    def CalculateOrder(self):
        #Type Node_Source defaults to order 1 at initilisation
        #Now need to loop through other objects to find correct ordering
        changes = 1
        while changes == 1:
            changes = 0
            for node in self.nodeList:
                if node.order == 0:
                    if node.GetParentOrder() != 0:
                        node.order = node.GetParentOrder() + 1
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
                node.append_to_dict(dict)

        for route in self.routeList:
            route.append_to_dict(dict)

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

    def LoadRoutes(self):
        with open('data/route.json', 'r') as file:
            data = json.load(file)

        for route in data["routes"]:
            obj = Route(route)
            self.routeList.append(obj)

    def SetupRoutes(self):
        for route in self.routeList:
            route.SetupRoute(self)

    def HandleClick(self, x, y):
        for node in self.nodeList:
            if isinstance(node, Node_Point):
                abs_dif_x = abs(x - int(node.x))
                abs_dif_y = abs(y - int(node.y))

                if (abs_dif_x < 1 and abs_dif_y < 1):
                    print(node.id + ' clicked')
                    node.switch()
                    self.i2c.SendState(node.node, node.point, node.point_state - 1)
                    return 1
                
        for route in self.routeList:
            if route.position_in_button(x, y):
                print(f"Route ID: '{route.id}' clicked")
                route.toggle()
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
