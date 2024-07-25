from procedure_data_tool.utils.node import Node

class Pump(Node):
    directions = 1
    def __init__(self, ein, pit = None, jumper = None, field_label = None, dvi = None):
        super().__init__(ein, pit = pit, jumper = jumper, field_label= field_label) 
        self.ein = ein
        self.directions = 100 
        self.node_1 = None
        self.connections = []
        self.show = True
        self.dvi_credited 
        self.dvi_used = "NO"
        self.in_tank = True
        self.color = "mediumpurple"

        def linkDVI(self, caller = None, stop = False):
            dvi_items = []
            return dvi_items
