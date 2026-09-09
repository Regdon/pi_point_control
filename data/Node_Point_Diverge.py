from .Node import Node

import static

class Node_Point_Diverge(Node):
    def __init__(self, id, x, y, parent_id, child_straight_id, child_turnout_id, point_default_state):
        Node.__init__(self, id, x, y, parent_id)

        self.child_straight_id = child_straight_id
        self.child_turnout_id = child_turnout_id
        self.point_default_state = point_default_state
        self.point_state = int(point_default_state)

    def GetDrawColour(self, child_node_id):
        if self.point_state == static.POINT_STATE_STRAIGHT and child_node_id == self.child_straight_id:
            return self.draw_colour
        elif self.point_state == static.POINT_STATE_TURNOUT and child_node_id == self.child_turnout_id:
            return self.draw_colour
        return static.COLOUR_DEFAULT

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
