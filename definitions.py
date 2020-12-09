from enum import Enum

# structural advice on class organization from acquaintance but code self-written

class AppPage(Enum):
    Home = 1
    Options = 2
    Graph = 3
    Twitter = 4
    Info = 5

class GraphMode(Enum):
    Histogram = 1
    Scatter = 2
    Bar = 3
    Groups = 4

class GraphOptions:
    def __init__(self):
        self.mode = None
        self.x = None
        self.y = None
        self.group = None
        self.scatterOffsetX = 0
        self.scatterOffsetY = 0
        self.prevScatterOffsetX = 0
        self.prevScatterOffsetY = 0
        self.zoomFactor = 1.0
