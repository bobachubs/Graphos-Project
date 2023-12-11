# organizes the pages (and its variables) of the app to be called conveniently
# Enum is a python class used for enumerations
# class structure taught by acquaintance but code and implementation self-written
# However, an example can be found online: https://www.tutorialspoint.com/enum-in-python
from enum import Enum

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
