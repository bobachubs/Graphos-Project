from color_manager import *
from cmu_112_graphics import *
from common import *
from data_manager import *
from enum import Enum
from graph_page import *
from home_page import *
from image_manager import *
from options_page import *

def mousePressed(app, event):
    if app.page == AppPage.Home:
        # todo: values should be variables imported
        homePageMousePressed(app, event)
    elif app.page == AppPage.Options:
        optionsPageMousePressed(app, event)
    elif app.page == AppPage.Graph:
        graphPageMousePressed(app, event)


def keyPressed(app, event):
    if event.key == 'm':
        app.animate = False
        if app.options.mode == GraphMode.Histogram:
            app.options.mode = GraphMode.Scatter
        elif app.options.mode == GraphMode.Scatter:
            app.options.mode = GraphMode.Bar
        elif app.options.mode == GraphMode.Bar:
            app.options.mode = GraphMode.Groups
        elif app.options.mode == GraphMode.Groups:
            app.options.mode = GraphMode.Histogram
    elif app.options.mode == GraphMode.Groups:
        if event.key == 'Space':
            app.animate = not app.animate
        elif event.key == 's':
            app.groupIdx += 1

def timerFired(app):
    if app.animate:
        app.groupIdx += 1

def appStarted(app):
    app.page = AppPage.Home
    app.colorManager = ColorManager()
    app.imageManager = ImageManager.load(app)
    # Home
    app.dataPath = None

    # Options
    app.options = GraphOptions()

    # Graph
    app.data = DataSet.load('nba_stats.csv')
    app.animate = False
    app.groupIdx = 1

def redrawAll(app, canvas):
    if app.page == AppPage.Home:
        drawHome(app, canvas)
    if app.page == AppPage.Options:
        drawOptions(app, canvas)
    elif app.page == AppPage.Graph:
        if app.options.mode == GraphMode.Histogram:
            drawHistogram(app, canvas)
        elif app.options.mode == GraphMode.Scatter:
            drawScatter(app, canvas)
        elif app.options.mode == GraphMode.Bar:
            drawBar(app, canvas)
        elif app.options.mode == GraphMode.Groups:
            drawGroups(app, canvas)

def main():
    runApp(width=1280, height=800)

if __name__ == '__main__':
    main()
