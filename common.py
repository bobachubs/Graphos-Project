from enum import Enum

class AppPage(Enum):
    Home = 1
    Options = 2
    Graph = 3

class GraphMode(Enum):
    Histogram = 1
    Scatter = 2
    Bar = 3
    Timeline = 4

class GraphOptions:
    def __init__(self):
        self.mode = None
        self.x = None
        self.y = None
