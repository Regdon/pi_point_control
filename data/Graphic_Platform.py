import static


class Graphic_Platform:
    def __init__(self, data):
        self.x1 = float(data["x1"])
        self.y1 = float(data["y1"])
        self.x2 = float(data["x2"])
        self.y2 = float(data["y2"])
        self.colour = data["Colour"]
        self.text = data["Text"]
        self.text_colour = data["Text-Colour"]

    def GetDrawScript(self):
        return {
            "type": "platform",
            "x1": self.x1 * static.GRID_SIZE_X,
            "y1": self.y1 * static.GRID_SIZE_Y,
            "x2": self.x2 * static.GRID_SIZE_X,
            "y2": self.y2 * static.GRID_SIZE_Y,
            "colour": self.colour,
            "text": self.text,
            "text_colour": self.text_colour,
        }
