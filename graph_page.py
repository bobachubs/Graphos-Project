from PIL import Image, ImageTk
from definitions import *

rates = [
    (0.5, 150),
    (1.0, 100),
    (2.0, 50),
    (4.0, 0),
]

zoomFactors = [
    0.5, 0.75, 1.0, 1.5, 2.0, 3.0,
]

def drawBackButton(app, canvas):
    canvas.create_image(75, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))

# set the 4 visual rate option rectangle bounds/rate
def rateButtonPositions():
    positions = []
    x = 1050
    y = 40
    boxWidth = 40
    boxHeight = 30
    for _ in rates:
        positions.append((x, y, x + boxWidth, y + boxHeight))
        x += boxWidth
    return positions

# draw the visual rate bounds
def drawVisualRates(app, canvas):
    for (idx, (x0, y0, x1, y1)) in enumerate(rateButtonPositions()):
        rate = rates[idx][0]
        delay = rates[idx][1]
        canvas.create_rectangle(x0, y0, x1, y1, fill='black' if app.timerDelay == delay else 'white')
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=f'{rate}X', font='Arial 16', fill='white' if app.timerDelay == delay else 'black')

def zoomButtonPositions():
    positions = []
    x = 800
    y = 40
    boxWidth = 40
    boxHeight = 30
    for _ in zoomFactors:
        positions.append((x, y, x+boxWidth, y+boxHeight))
        x += boxWidth
    return positions

def drawZoomOptions(app, canvas):
    for (idx, (x0, y0, x1, y1)) in enumerate(zoomButtonPositions()):
        zoom = zoomFactors[idx]
        canvas.create_rectangle(x0, y0, x1, y1, fill='black' if app.options.zoomFactor == zoom else 'white')
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=f'{zoom}x', font='Arial 16', fill='white' if app.options.zoomFactor == zoom else 'black')

def graphPageMousePressed(app, event):
    if 50 < event.x < 100 and 30 < event.y < 70:
        app.page = AppPage.Options
        # reset group animation
        app.groupIdx = 1
        app.animate = False
        app.options.scatterOffsetX = 0
        app.options.scatterOffsetY = 0
        app.options.prevScatterOffsetX = 0
        app.options.prevScatterOffsetY = 0
        app.options.zoomFactor = 1.0

    # click on visual rate
    if app.options.mode == GraphMode.Groups:
        for (idx, (x0, y0, x1, y1)) in enumerate(rateButtonPositions()):
            if x0 < event.x < x1 and y0 < event.y < y1:
                app.timerDelay = rates[idx][1]

    if app.options.mode == GraphMode.Scatter:
        # Scatter dragging
        pad = 40
        graphWidth = app.width - pad * 2
        graphHeight = app.height - pad * 4
        graphX0 = pad
        graphY0 = app.height - pad - graphHeight
        graphX1 = pad + graphWidth
        graphY1 = app.height - pad
        if graphX0 < event.x < graphX1 and graphY0 < event.y < graphY1:
            app.isScatterDragging = True

        # Scatter zoom
        for (idx, (x0, y0, x1, y1)) in enumerate(zoomButtonPositions()):
            if x0 < event.x < x1 and y0 < event.y < y1:
                app.options.zoomFactor = zoomFactors[idx]

def graphPageMouseReleased(app, event):
    app.isScatterDragging = False
    app.options.prevScatterOffsetX = app.options.scatterOffsetX
    app.options.prevScatterOffsetY = app.options.scatterOffsetY

def graphPageMouseDragged(app, event):
    if app.isScatterDragging:
        app.options.scatterOffsetX = event.x - app.mousePressedEvent.x + app.options.prevScatterOffsetX
        app.options.scatterOffsetY = event.y - app.mousePressedEvent.y + app.options.prevScatterOffsetY

def drawHistogram(app, canvas):
    drawBackButton(app, canvas)
    histogramBuckets = app.data.getHistogram(app.options.x)
    maxValue = max([e[1] for e in histogramBuckets])
    pad = 40

    graphWidth = app.width - pad * 2
    barWidth = graphWidth / len(histogramBuckets)
    graphHeight = app.height - pad * 4
    heightRatio = graphHeight / maxValue

    x0 = pad
    for (time, value) in histogramBuckets:
        y0 = app.height - pad
        x1 = x0 + barWidth
        y1 = y0 - value * heightRatio
        color = app.colorManager.getColor(time)

        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        canvas.create_text((x0 + x1) / 2, y0 + pad / 2, text=time)
        canvas.create_text((x0 + x1) / 2, y1 - pad / 2, text=str(value))
        x0 += barWidth

    canvas.create_text(app.width/2, 20, text=f'Histogram - {app.options.x}', font='Arial 16')

# turned regression math into code
# https://www.kosbie.net/ml/04-05/honors-precalc/linearRegression.htm
def drawRegressionLine(app, canvas):
    (points, xMin, xMax, yMin, yMax) = app.data.getScatterData(app.options.x, app.options.y)

    pad = 40
    graphWidth = app.width - pad * 2
    widthRatio = graphWidth / (xMax - xMin)
    graphHeight = app.height - pad * 4
    heightRatio = graphHeight / (yMax - yMin)

    canvas.create_text(pad, app.height - pad - graphHeight - 20, text=app.options.y)

    # linear regression line
    xList, yList = [], []

    for (px, py) in points:
        x = pad + (px - xMin)*widthRatio + app.options.scatterOffsetX
        y = app.height-pad-(py-yMin)*heightRatio + app.options.scatterOffsetY
        xList += [x]
        yList += [y]

    meanX = 0 if not xList else sum(xList)/len(xList)
    meanY = 0 if not yList else sum(yList)/len(yList)

    SSxx = 0
    SSxy = 0

    for idx in range(max(len(xList), len(yList))):
        SSxx += (xList[idx]-meanX)**2
        SSxy += (yList[idx]-meanY)*(xList[idx]-meanX)

    slope = SSxy/SSxx

    b = meanY - slope * meanX

    pointStartX, pointEndX = 0, graphWidth
    pointStartY, pointEndY = (slope*(0+pad) + b), (slope*(pad + graphWidth) + b)
    canvas.create_line(pad + pointStartX, pointStartY,
                       pad + graphWidth, pointEndY)

def drawRegressionEquation(app, canvas):
    (points, xMin, xMax, yMin, yMax) = app.data.getScatterData(app.options.x, app.options.y)

    xList, yList = [], []

    for (px, py) in points:
        xList += [px]
        yList += [py]


    meanX = 0 if not xList else sum(xList)/len(xList)
    meanY = 0 if not yList else sum(yList)/len(yList)

    SSxx = 0
    SSxy = 0

    for idx in range(max(len(xList), len(yList))):
        SSxx += (xList[idx]-meanX)**2
        SSxy += (yList[idx]-meanY)*(xList[idx]-meanX)

    slope = round(SSxy/SSxx, 2)
    b = round(meanY - slope * meanX, 2)
    canvas.create_text(200, 50, text = f'{app.options.y} = {slope}*{app.options.x} + {b}', anchor = 'w', font = 'Arial 18')

def drawScatter(app, canvas):
    # title
    canvas.create_text(app.width/2, 20, text=f'Scatterplot - {app.options.x}-{app.options.y}', font='Arial 16')
    drawBackButton(app, canvas)
    drawZoomOptions(app, canvas)

    # graph
    (points, xMin, xMax, yMin, yMax) = app.data.getScatterData(app.options.x, app.options.y)

    xDiff = (xMax - xMin) * (1 - (1 / app.options.zoomFactor)) / 2
    yDiff = (yMax - yMin) * (1 - (1 / app.options.zoomFactor)) / 2
    xMin += xDiff
    xMax -= xDiff
    yMin += yDiff
    yMax -= yDiff

    pad = 40
    graphWidth = app.width - pad * 2
    widthRatio = graphWidth / (xMax - xMin)
    graphHeight = app.height - pad * 4
    heightRatio = graphHeight / (yMax - yMin)

    # x-axis
    canvas.create_line(pad, app.height - pad - graphHeight, pad, app.height - pad)
    canvas.create_text(app.width / 2, app.height - pad/4, text=app.options.x)
    xMinLabel = str(round((xMin - app.options.scatterOffsetX/widthRatio), 2))
    x2ndLabel = str(round((xMin + (xMax-xMin)/4 - app.options.scatterOffsetX/widthRatio), 2))
    xMidLabel = str(round((xMin + (xMax - xMin)/2 - app.options.scatterOffsetX/widthRatio), 2))
    x4thLabel = str(round((xMin + .75*(xMax - xMin) - app.options.scatterOffsetX/widthRatio), 2))
    xMaxLabel = str(round((xMax - app.options.scatterOffsetX/widthRatio), 2))
    canvas.create_text(pad, app.height - pad + 5, text=xMinLabel, anchor='n', font='Arial 10')
    canvas.create_text(pad+graphWidth/4, app.height - pad + 5, text=x2ndLabel, anchor='n', font='Arial 10')
    canvas.create_text(pad + graphWidth / 2, app.height - pad + 5, text=xMidLabel, anchor='n', font='Arial 10')
    canvas.create_text(pad + .75 * graphWidth, app.height - pad + 5, text=x4thLabel, anchor='n', font='Arial 10')
    canvas.create_text(pad + graphWidth, app.height - pad + 5, text=xMaxLabel, anchor='n', font='Arial 10')
    x = pad
    for _ in range(7):
        x += graphWidth / 8
        canvas.create_line(x, app.height - pad - 5, x, app.height - pad + 5)

    # y-axis
    canvas.create_line(pad, app.height - pad, app.width - pad, app.height - pad)
    canvas.create_text(pad, app.height - pad - graphHeight - 20, text=app.options.y)
    yMinLabel = str(round((yMin + app.options.scatterOffsetY/heightRatio), 2))
    y2ndLabel = str(round((yMin + (yMax-yMin)/4 + app.options.scatterOffsetY/heightRatio), 2))
    yMidLabel = str(round((yMin + (yMax - yMin)/2 + app.options.scatterOffsetY/heightRatio), 2))
    y4thLabel = str(round((yMin + .75*(yMax - yMin) + app.options.scatterOffsetY/heightRatio), 2))
    yMaxLabel = str(round((yMax + app.options.scatterOffsetY/heightRatio), 2))
    canvas.create_text(pad - 5, app.height - pad, text=yMinLabel, anchor='e', font='Arial 10')
    canvas.create_text(pad - 5, app.height - pad - graphHeight / 4, text=y2ndLabel, anchor='e', font='Arial 10')
    canvas.create_text(pad - 5, app.height - pad - graphHeight / 2, text=yMidLabel, anchor='e', font='Arial 10')
    canvas.create_text(pad - 5, app.height - pad - .75 * graphHeight, text=y4thLabel, anchor='e', font='Arial 10')
    canvas.create_text(pad - 5, app.height - pad - graphHeight, text=yMaxLabel, anchor='e', font='Arial 10')
    y = app.height - pad - graphHeight
    for _ in range(7):
        y += graphHeight / 8
        canvas.create_line(pad - 5, y, pad + 5, y)

    # graph points
    ex, ey = 0, 0
    if app.mouseMovedEvent:
        ex, ey = app.mouseMovedEvent.x, app.mouseMovedEvent.y
    for (px, py) in points:
        x = pad + (px - xMin) * widthRatio + app.options.scatterOffsetX
        y = app.height - pad - (py - yMin) * heightRatio + app.options.scatterOffsetY

        if not (pad <= x <= pad + graphWidth) or not (app.height - pad - graphHeight <= y <= app.height - pad):
            continue

        hovered = x-2 < ex < x+2 and y-2 < ey < y+2
        canvas.create_oval(x-2, y-2, x+2, y+2, fill='red' if hovered else 'light blue')
        if not app.isScatterDragging and hovered:
            canvas.create_text(x + 10, y + 10, text=f'({px},{py})', font='Arial 14', anchor='w')

    # linear regression
    #drawRegressionLine(app, canvas)
    #drawRegressionEquation(app, canvas)

def drawBar(app, canvas):
    drawBackButton(app, canvas)
    aggregates = app.data.getAggregates(app.options.x, app.options.y)
    # inspiration and guidance on how to use from acquaintance as well as 
    # https://stackoverflow.com/questions/16310015/what-does-this-mean-key-lambda-x-x1
    # lines 213, 241
    leaders = sorted(aggregates.items(), key=lambda p: p[1], reverse=True)[:10]

    # Draw rectangles from the left proportional to the target ratio
    fullWidth = app.width - 40
    topStat = leaders[0][1]
    ratio = fullWidth / topStat * 0.8

    h = 100
    for (xvar, yvar) in leaders:
        x0 = 20
        y0 = h
        x1 = 20 + yvar * ratio
        y1 = h + 50
        color = app.colorManager.getColor(xvar)

        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=xvar, font='Arial 12')
        canvas.create_text(x1 + 20 , (y0 + y1) / 2, text=f'{str(round(yvar, 2))}', font='Arial 12')
        h += 60

    canvas.create_text(app.width/2, 20, text=f'Bar - {app.options.y} by {app.options.x}', font='Arial 16')

def drawGroups(app, canvas):
    drawBackButton(app, canvas)
    drawVisualRates(app, canvas)
    groups = app.data.getAggregatesGroups(app.options.x, app.options.y, app.options.group)
    idx = min(len(groups)-1, app.groupIdx)
    (group, aggregates) = groups[idx]
    leaders = sorted(aggregates.items(), key=lambda p: p[1], reverse=True)[:10]

    # Draw rectangles from the left proportional to the target ratio
    fullWidth = app.width - 40
    topStat = leaders[0][1]
    ratio = 0 if topStat == 0 else fullWidth / topStat * 0.8

    h = 100
    for (xvar, yvar) in leaders:
        x0 = 20
        y0 = h
        x1 = 20 + yvar * ratio
        y1 = h + 50
        color = app.colorManager.getColor(xvar)

        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=xvar, font='Arial 12')
        canvas.create_text(x1 + 20 , (y0 + y1) / 2, text=f'{str(round(yvar, 2))}', font='Arial 12')
        h += 60

    canvas.create_text(app.width/2, 20, text=f'{app.options.y} by {app.options.x} over {app.options.group}', font='Arial 20')
    canvas.create_text(app.width/2, 55, text=f'(P to Start/Pause and S to Step)', font='Arial 12')
    canvas.create_text(280, 50, text=f'{app.options.group} : {group}', font='Arial 18', anchor='w')
