import static


class Graphic_Tunnel:
    def __init__(self, data):
        self.x = float(data["x1"])
        self.y = float(data["y1"])
        self.radius = float(data["radius"])
        self.orientation = float(data["orientation"])
        self.colour = data["Colour"]

    def GetDrawScript(self):
        return {
            "type": "tunnel",
            "x": self.x * static.GRID_SIZE_X,
            "y": self.y * static.GRID_SIZE_Y,
            "radius": self.radius * static.GRID_SIZE_X,
            "orientation": self.orientation,
            "colour": self.colour,
        }
