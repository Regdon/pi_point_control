from .Node import Node

import static

class Node_Point_Diverge(Node):
    def __init__(self, id, x, y, parent_id, child_straight_id, child_turnout_id, point_default_state):
        Node.__init__(self, id, x, y, parent_id)

        self.child_straight_id = child_straight_id
        self.child_turnout_id = child_turnout_id
        self.point_default_state = point_default_state
        self.point_state = point_default_state

    def GetDrawColour(self, child_node_id):
        if self.point_state == static.POINT_STATE_STRAIGHT and child_node_id == self.child_straight_id:
            return self.draw_colour
        elif self.point_state == static.POINT_STATE_TURNOUT and child_node_id == self.child_turnout_id:
            return self.draw_colour
        return None
