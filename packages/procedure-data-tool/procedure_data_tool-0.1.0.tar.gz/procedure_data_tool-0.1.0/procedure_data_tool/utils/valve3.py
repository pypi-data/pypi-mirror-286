from procedure_data_tool.utils.valve import Valve

class Valve3(Valve):
    directions = 3
    blocked_element = None
    def __init__(self, ein, pit = None, jumper = None, field_label = None, dvi = None):
        super().__init__(ein, pit= pit, jumper = jumper, field_label= field_label)
        self.directions = 3
        self.ein = ein
        self.connections = []
        self.show = True
        self.in_tank = False
        self.position
        self.dvi_credited = dvi
        self.blocked_element

    def setBlockedElement(self, route):
        for connection in self.connections:
            if connection in route:
                pass
            else:
                self.blocked_element = connection

    def markPosition(self):
        if self.blocked_element:
            if self.blocked_element.EIN():
                self.position = "BLOCK " +  self.blocked_element.EIN()
            else:
                for next_connection in self.blocked_element.connections:
                    if next_connection == self or next_connection in self.connections:
                        pass
                    else:
                        self.position = "BLOCK " + next_connection.EIN()

    def setPosition(self, route = None):
        self.setBlockedElement(route=route)
        self.markPosition()

    def linkDVI(self, caller=None, stop = False):
        dvi_items = []
        self.dvi_used = self.dvi_credited
        if self.dvi_credited == "YES":
            self.blocked_element = caller
            self.markPosition()
            dvi_items.append(self)
        elif self.dvi_credited == "POS":
            dvi_items.append(self)
            for connection in self.connections:
                if connection == caller:
                    pass
                else:
                    self.blocked_element = connection
                    self.markPosition()
                    break
            for connection in self.connections:
                if connection == caller or connection == self.blocked_element:
                    pass
                else:
                    dvi_items.extend(connection.linkDVI(caller = self))
        elif self.dvi_credited == "NO":
            for connection in self.connections:
                if connection == caller:
                    pass
                else:
                    dvi_items.extend(connection.linkDVI(caller = self))
        else:
            pass
        return dvi_items

    def getDVI(self):
        dvi_elements = []
        if self.blocked_element:
            dvi_elements.extend(self.blocked_element.linkDVI(caller = self))
        if dvi_elements:
            self.dvi_used = self.dvi_credited 
        else:
            self.dvi_used = "NO"
        return dvi_elements
    
    def getColor(self):
        if (self.dvi_used == "YES"):
            self.color = "steelblue"
        elif (self.dvi_used == "POS"):
            self.color = "indianred"
        if (self.dvi_used == "NO"):
            self.color = "lightgray"
        return self.color