from procedure_data_tool.utils.node import Node

class Line(Node):
    directions = 1
    def __init__(self, ein, pit = None, jumper = None, field_label = None, dvi = None):
        super().__init__(ein, pit = pit, jumper = jumper, field_label= field_label) 
        self.ein = ein
        self.directions = 2
        self.node_1 = None
        self.connections = []
        self.show = True
        self.dvi_credited 
        self.dvi_used = "NO"
        self.in_tank = False
        self.onJumper = False
        self.color = "white"
        self.size = 20
