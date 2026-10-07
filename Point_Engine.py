from data.Node import Node
from data.Node_Source import Node_Source
from data.Node_Point_Diverge import Node_Point_Diverge
from data.Node_Point_Converge import Node_Point_Converge
from data.config import validate_configuration
from data.route import Route

import json
from pathlib import Path

# from i2c import i2c_control

class Point_Engine:
    def __init__(self):
        self.node_list = []
        self.route_list = []
        self._route_data = None
        # self.i2c = i2c_control()

    # def GetNodeByID(self, id):
    #     for node in self.nodeList:
    #         if (node.id == id):
    #             return node
            
    # def GetRoute(self, id_from, id_to):
    #     result = []

    #     node_current = self.GetNodeByID(id_from)
    #     # print(f"Starting routing for {node_current}")

    #     while True:            
    #         if (node_current.id == id_to):
    #             # print(f"Target node {node_current} found, stopping")
    #             result.append(node_current) 
    #             return result
    #         elif isinstance(node_current, Node_Source):
    #             #If we get here, no route has been found, return 0
    #             # print(f"Source node {node_current} found, unable to find target")
    #             return 0
    #         elif isinstance(node_current, Node_Point):
    #             if (node_current.point_type == static.POINT_TYPE_CONVERGE):
    #                 #This is the tricky siutation, because we don't know which way to go to our destination. 
    #                 route_straight = self.GetRoute(node_current.set_straight_id, id_to)
    #                 route_turnout = self.GetRoute(node_current.set_turnout_id, id_to)
    #                 if (route_straight):
    #                     # print(f"Following straight from point {node_current}")
    #                     result.append(node_current)
    #                     for part in route_straight:
    #                         result.append(part)
    #                     return result
    #                 elif (route_turnout):
    #                     # print(f"Following turnout from point {node_current}")
    #                     result.append(node_current)
    #                     for part in route_turnout:
    #                         result.append(part)
    #                     return result
    #                 else:
    #                     # print(f"Routing error from point {node_current}, this shouldn't happen")
    #                     return 0
    #             else:
    #                 # print(f"Divering point {node_current} found, continuing to parent")
    #                 result.append(node_current)
    #                 node_current = node_current.GetParent()                
    #         else:
    #             # print(f"node {node_current} found, continuing to parent")
    #             result.append(node_current)
    #             node_current = node_current.GetParent()
            
    # def Setup(self):
    #     for node in self.nodeList:
    #         node.Setup(self.nodeList)

    # def CalculateOrder(self):
    #     #Type Node_Source defaults to order 1 at initilisation
    #     #Now need to loop through other objects to find correct ordering
    #     changes = 1
    #     while changes == 1:
    #         changes = 0
    #         for node in self.nodeList:
    #             if node.order == 0:
    #                 if node.GetParentOrder() != 0:
    #                     node.order = node.GetParentOrder() + 1
    #                     changes = 1

    # def ResetState(self):
    #     for node in self.nodeList:
    #         node.state = "None"

    # def CalculateState(self):
    #     self.ResetState()

    #     for node in self.nodeList:
    #         node.CalculateState()

    #     for route in self.routeList:
    #         route.CheckBlocked()
            

    def SetupAllNodeParents(self):
        for node in self.node_list:
            node.SetupParent(self.node_list)

    def CalculateAllNodeDrawColours(self):
        for node in self.node_list:
            node.CalculateDrawColour()

    def GetAllDrawScripts(self):
        dict = []
        for node in self.node_list:
            value = node.GetDrawScript()
            if value is not None:
                if isinstance(value, list):
                    dict.extend(value)
                else:
                    dict.append(value)

        for route in self.route_list:
            dict.append(route.GetDrawScript())

        return json.dumps(dict)

    def LoadData(self):
        data_directory = Path(__file__).resolve().parent / 'data'
        with (data_directory / 'node_data.json').open(
            'r', encoding='utf-8'
        ) as file:
            node_data = json.load(file)

        with (data_directory / 'route_data.json').open(
            'r', encoding='utf-8'
        ) as file:
            route_data = json.load(file)

        validate_configuration(node_data, route_data)
        self._route_data = route_data

        for node in node_data["nodes"]:
            if (node["type"] == "node"):
                obj = Node(node["id"], node["x"], node["y"], node["parent"])
                self.node_list.append(obj)

            if (node["type"] == "node_source"):
                obj = Node_Source(node["id"], node["x"], node["y"], node["colour"])
                self.node_list.append(obj)
            
            if (node["type"] == "node_point_diverge"):
                obj = Node_Point_Diverge(
                    node["id"], node["x"], node["y"], node["parent"],
                    node["child_straight_id"], node["child_turnout_id"],
                    node["point_default_state"], node["node"], node["point"],
                )
                self.node_list.append(obj)

            if (node["type"] == "node_point_converge"):
                obj = Node_Point_Converge(
                    node["id"], node["x"], node["y"],
                    node["parent_straight_id"], node["parent_turnout_id"],
                    node["point_default_state"], node["node"], node["point"],
                )
                self.node_list.append(obj)

    def LoadRoutes(self):
        if self._route_data is None:
            raise RuntimeError("LoadData must be called before LoadRoutes")

        route_data = self._route_data
        for route in route_data["routes"]:
            obj = Route(route)
            self.route_list.append(obj)

    def SetupRoutes(self):
        for route in self.route_list:
            route.SetupRoute(self.node_list)

    def HandleClick(self, x, y):
        print("----------Button Click-------------")
        for node in self.node_list:
            if node.HandleClick(x, y):
                print(f"Node ID: '{node.id}' clicked")
                return 1
                
        for route in self.route_list:
            if route.HandleClick(x, y):
                print(f"Route ID: '{route.id}' clicked")
                return 1

        return 0

    def CalculateAllRouteStates(self):
        for route in self.route_list:
            route.CalculateState()


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
