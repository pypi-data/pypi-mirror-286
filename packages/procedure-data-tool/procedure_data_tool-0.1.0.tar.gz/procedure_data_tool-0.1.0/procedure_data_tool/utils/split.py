from procedure_data_tool.utils.node import Node

class Split(Node):
    directions = 3
    branching_element = None
    def __init__(self, ein, pit = None, jumper = None, field_label = None, dvi = None):
        super().__init__(ein, pit, jumper, field_label= field_label)
        self.directions = 3; 
        self.ein = ein
        self.connections = []
        self.show = False
        self.in_tank = False
        self.onJumper = False
        self.color = "white"
        self.branching_element

    def setBranchingElement(self, route):
        for connection in self.connections:
            if connection in route:
                pass
            else:
                self.branching_element = connection
    def EIN(self):
        return None

    def setPosition(self, route = None):
        self.setBranchingElement(route=route)

    def linkDVI(self, caller=None, stop = False):
        dvi_items = []
        dvi_items.append(self)
        for connection in self.connections:
            if connection == caller:
                pass
            else:
                dvi_items.extend(connection.linkDVI(caller = self, stop = True))
        return dvi_items

    def getDVI(self):
        dvi_elements = []
        if self.branching_element:
            dvi_elements.extend(self.branching_element.linkDVI(caller = self))
        return dvi_elements