from .Node_Point import Node_Point

import static

class Toggle:
    def __init__(self, data, engine):
        # id
        if "id" in data:
            self.id = data["id"]
        else:
            self.id = ""
        self.engine = engine

        # button properties
        if "button_position_x" in data:
            self.button_position_x = int(data["button_position_x"])
        else:
            self.button_position_x = 0
            
        if "button_position_y" in data:
            self.button_position_y = int(data["button_position_y"])
        else:
            self.button_position_y = 0

        if "button_colour_default" in data and "button_colour_toggle" in data:
            self.button_colour = [data["button_colour_default"], data["button_colour_toggle"]]
        else:
            self.button_colour = ["#000000", "#000000"]

        # toggle properties
        self.state = 0
        self.toggle_points = []

    def AddNode(self, node_id, turnout_state):
        node = self.engine.GetNodeByID(node_id)
        item = ToggleItem(node, turnout_state)
        self.toggle_points.append(item)

    def Toggle(self):        
        if (self.state == 0):
            self.state = 1
        else:
            self.state = 0
        
        for point in self.toggle_points:
            point.setState(self.state)

    def GetButtonJSON(self, dict):
        dict.append({
            "type": "route_button"
            ,"x1": self.button_position_x * static.GRID_SIZE_X
            ,"y1": self.button_position_y * static.GRID_SIZE_Y
            ,"width": 4 * static.GRID_SIZE_X
            ,"height": 2 * static.GRID_SIZE_Y
            ,"colour": self.GetColour()
            ,"active": self.state
        })

    def GetColour(self):
        return self.button_colour[self.state]

    def IsClicked(self, x, y):
        return (x >= self.button_position_x and y >= self.button_position_y and x <= self.button_position_x + 4 and y <= self.button_position_y + 2)


class ToggleItem:
    def __init__(self, node, state_toggled):
        self.node = node
        if (state_toggled == "Turnout"):
            self.state_default = static.POINT_STATE_STRAIGHT
            self.state_toggled = static.POINT_STATS_TURNOUT
        else:
            self.state_default = static.POINT_STATS_TURNOUT
            self.state_toggled = static.POINT_STATE_STRAIGHT
        self.state = 0

    def setState(self, value):
        self.state = value
        if (self.state == 0):
            self.node.SetPointState(self.state_default)
        else:
            self.node.SetPointState(self.state_toggled)
        
