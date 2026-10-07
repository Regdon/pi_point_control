from .Node_Point import Node_Point

import static

class Node_Point_Diverge(Node_Point):
    def __init__(
        self,
        id,
        x,
        y,
        parent_id,
        child_straight_id,
        child_turnout_id,
        point_default_state,
        node,
        point,
    ):
        Node_Point.__init__(
            self, id, x, y, parent_id, point_default_state, node, point
        )

        self.child_straight_id = child_straight_id
        self.child_turnout_id = child_turnout_id

    def GetDrawColour(self, child_node_id):
        if self.point_state == static.POINT_STATE_STRAIGHT and child_node_id == self.child_straight_id:
            return self.draw_colour
        elif self.point_state == static.POINT_STATE_TURNOUT and child_node_id == self.child_turnout_id:
            return self.draw_colour
        return static.COLOUR_DEFAULT
