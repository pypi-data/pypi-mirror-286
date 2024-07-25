from collections import deque

class Node:
    connections = []
    directions = 0
    pit = None
    jumper = None
    jumperLabel = None
    position = None
    onJumper = True
    dvi_credited = None
    dvi_used = None
    in_tank = False
    color = 'lightgray'
    size = 50
    field_label = None
    def __init__(self, ein, pit, jumper, field_label):
        self.ein = ein
        self.pit = pit
        self.jumper = jumper
        self.field_label = field_label
        self.directions
        self.connections
        # self.dvi_used
        self.show = True
        self.in_tank = False
        self.dvi_credited = None
        self.dvi_used = None
        self.jumperLabel
        self.position
        self.onJumper
        self.color
        # self.size
    
    def EIN(self):
        return self.ein
    
    def __str__(self):
        return self.ein
    
    def setPit(self, str):
        self.pit = str

    def setJumper(self, jumper):
        self.jumper = jumper

    def linkDVI(self, caller = None, stop = False):
        dvi_items = [self]
        for connection in self.connections:
            if connection == caller:
                pass
            else: 
                dvi_items.extend(connection.linkDVI(caller = self))
        if len(dvi_items) == 1:
            return []
        return dvi_items
    
    def setPosition(self, route = None, forced = None):
        return
    
    def getColor(self):
        return self.color

    def connectBack(self, node):
        if node in self.connections: return
        elif len(self.connections) < self.directions: self.connect(node)
        else: 
            print(self.EIN(), "has maximum number of connections, cant connect back")
            print(type(self))
            for con in self.connections:
                print(con.EIN())
        return

    def connect(self, *nodes):
        for node in nodes[:self.directions]:
            if node and node not in self.connections:
                if len(self.connections) <= self.directions:
                    self.connections.append(node)
                    node.connectBack(self)
                else:  
                    print("has maximum number of connections", self.EIN())
                    for connection in self.connections:
                        print(connection.EIN())

    def report(self):
        print((self.EIN()), "connections: ")
        for node in self.connections:
            if (node):
                print(node.EIN())
            else:
                print("Missing Connection")
    
    def routesTo(self, target, num_routes = 1, exclude_target = None):
        paths = []
        queue = deque([[self]])

        while queue and len(paths) < num_routes:
            path = queue.popleft()
            node = path[-1]

            if node == target:
                if path not in paths:
                    paths.append(path)
                
            for connection in node.connections :
                if connection not in path and (exclude_target is None or exclude_target not in path):
                    queue.append(path + [connection])

        return paths