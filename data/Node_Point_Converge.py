from .Node import Node

import static

class Node_Point_Converge(Node):
    def __init__(self, id, x, y, parent_straight_id, parent_turnout_id, point_default_state):
        Node.__init__(self, id, x, y, None)

        self.parent_straight_id = parent_straight_id
        self.parent_turnout_id = parent_turnout_id
        self.point_default_state = point_default_state
        self.point_state = int(point_default_state)

    def SetupParent(self, node_list):
        for node in node_list:
            if node.id == self.parent_straight_id:
                self.parent_straight_id = node
            elif node.id == self.parent_turnout_id:
                self.parent_turnout_id = node
        return 1

    def GetDrawScript(self):
        returnValue = []
        if self.point_state == static.POINT_STATE_STRAIGHT:
            colour = self.draw_colour
        else:
            colour = static.COLOUR_DEFAULT

        returnValue.append({"x1": self.GetGridX(), "y1": self.GetGridY(), 'x2': self.parent_straight_id.GetGridX(), "y2": self.parent_straight_id.GetGridY(),"colour": colour})

        if self.point_state == static.POINT_STATE_TURNOUT:
            colour = self.draw_colour
        else:
            colour = static.COLOUR_DEFAULT

        returnValue.append({"x1": self.GetGridX(), "y1": self.GetGridY(), 'x2': self.parent_turnout_id.GetGridX(), "y2": self.parent_turnout_id.GetGridY(),"colour": colour})

        return returnValue

    def CalculateDrawColour(self):
        if self.point_state == static.POINT_STATE_STRAIGHT:
            self.draw_colour = self.parent_straight_id.GetDrawColour(self.id)
        else:
            self.draw_colour = self.parent_turnout_id.GetDrawColour(self.id)

    def HandleClick(self, gridX, gridY):
        abs_dif_x = abs(gridX - int(self.x))
        abs_dif_y = abs(gridY - int(self.y))

        if (abs_dif_x < 1 and abs_dif_y < 1):
            print(self.id + ' clicked')
        else:
            return 0

        if self.point_state == static.POINT_STATE_STRAIGHT:
            self.point_state = static.POINT_STATE_TURNOUT
        else:
            self.point_state = static.POINT_STATE_STRAIGHT

        return 1
