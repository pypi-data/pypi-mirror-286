from procedure_data_tool.utils.node import Node

class Valve(Node):
    connections = []
    directions = 0
    def __init__(self, ein, pit = None, jumper = None, field_label = None, dvi = None):
        super().__init__(ein, pit= pit, jumper = jumper, field_label= field_label) 
        self.connections
        self.directions
        self.show = True
        self.in_tank = False
        self.jumper = jumper
        self.dvi_credited = dvi
                
        