class Route:
    def __init__(self, data):
        self.id = data["id"]
        self.node_id_start = data["node_id_start"]
        self.node_id_end = data["node_id_end"]
        self.position_x = int(data["position_x"])
        self.position_y = int(data["position_y"])
        self.align = data["align"]
        self.colour = data["colour"]

        self.route = []

    def SetupRoute(self, engine):
        self.route = engine.GetRoute(self.node_id_start, self.node_id_end)
        print(self.route)


