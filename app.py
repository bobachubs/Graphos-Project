# Run this file! Controls all the pages and events as a wrapper
from color_manager import *
from cmu_112_graphics import *
from data_manager import *
from definitions import *
from graph_page import *
from home_page import *
from image_manager import *
from options_page import *
from twitter_page import *
from info_page import *

def mousePressed(app, event):
    app.mousePressedEvent = event
    if app.page == AppPage.Home:
        homePageMousePressed(app, event)
    elif app.page == AppPage.Options:
        optionsPageMousePressed(app, event)
    elif app.page == AppPage.Graph:
        graphPageMousePressed(app, event)
    elif app.page == AppPage.Twitter:
        twitterPageMousePressed(app, event)
    elif app.page == AppPage.Info:
        infoPageMousePressed(app, event)

def mouseReleased(app, event):
    if app.page == AppPage.Graph:
        graphPageMouseReleased(app, event)

def mouseDragged(app, event):
    if app.page == AppPage.Graph:
        graphPageMouseDragged(app, event)

def mouseMoved(app, event):
    app.mouseMovedEvent = event

def keyPressed(app, event):
    if app.page == AppPage.Graph:
        if app.options.mode == GraphMode.Groups:
            if event.key == 'Space':
                app.animate = not app.animate
            elif event.key == 's':
                app.groupIdx += 1
    elif app.page == AppPage.Twitter:
        if event.key == 'Space':
            if not app.animate:
                app.data.run()
            else:
                app.data.stop()
            app.animate = not app.animate

def timerFired(app):
    if app.animate:
        app.groupIdx += 1

def appStarted(app):
    app.page = AppPage.Home
    app.colorManager = ColorManager()
    app.imageManager = ImageManager.load(app)
    app.mouseMovedEvent = None
    app.mousePressedEvent = None

    # Home
    app.dataPath = None

    # Options
    app.options = GraphOptions()

    # Graph
    app.animate = False
    app.groupIdx = 1
    app.timerDelay = 100
    app.isScatterDragging = False
    app.userZoomInput = 1

def appStopped(app):
    if app.page == AppPage.Twitter:
        app.data.stop()

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
            drawRegressionLine(app, canvas)
            drawRegressionEquation(app, canvas)
        elif app.options.mode == GraphMode.Bar:
            drawBar(app, canvas)
        elif app.options.mode == GraphMode.Groups:
            drawGroups(app, canvas)
    elif app.page == AppPage.Twitter:
        drawTwitter(app, canvas)
    elif app.page == AppPage.Info:
        drawInfo(app, canvas)

def main():
    runApp(width=1280, height=800)

if __name__ == '__main__':
    main()
