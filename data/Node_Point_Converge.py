from .Node_Point import Node_Point

import static

class Node_Point_Converge(Node_Point):
    def __init__(
        self,
        id,
        x,
        y,
        parent_straight_id,
        parent_turnout_id,
        point_default_state,
        node,
        point,
    ):
        Node_Point.__init__(
            self, id, x, y, None, point_default_state, node, point
        )

        self.parent_straight_id = parent_straight_id
        self.parent_turnout_id = parent_turnout_id

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
