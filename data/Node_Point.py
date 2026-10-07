from .Node import Node

import static


class Node_Point(Node):
    def __init__(
        self,
        id,
        x,
        y,
        parent_id,
        point_default_state,
        node,
        point,
        state_changed=None,
    ):
        Node.__init__(self, id, x, y, parent_id)

        self.point_default_state = point_default_state
        self.point_state = int(point_default_state)
        self.node = int(node)
        self.point = int(point)
        self.state_changed = state_changed
        self.locked = 0

    def HandleClick(self, gridX, gridY):
        abs_dif_x = abs(gridX - int(self.x))
        abs_dif_y = abs(gridY - int(self.y))

        if (abs_dif_x < 1 and abs_dif_y < 1):
            print(self.id + ' clicked')
        else:
            return 0

        return self.TogglePointState()

    def TogglePointState(self):
        if self.locked == 1:
            print(self.id + ' is locked')
            return 0

        if self.point_state == static.POINT_STATE_STRAIGHT:
            self.SetPointState(static.POINT_STATE_TURNOUT)
        else:
            self.SetPointState(static.POINT_STATE_STRAIGHT)
        return 1

    def SetPointState(self, point_state):
        if self.locked == 1:
            print(self.id + ' is locked')
            return 0

        if self.point_state == point_state:
            return 1

        self.point_state = point_state
        if self.state_changed is not None:
            self.state_changed(self.node, self.point, point_state)
        return 1

    def LockToState(self, point_state):
        self.SetPointState(point_state)
        self.locked = 1
        return 1

    def ClearLockedState(self):
        self.locked = 0
        return 1
