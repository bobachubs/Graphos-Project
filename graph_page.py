from PIL import Image, ImageTk
from common import *

def drawBackButton(app, canvas):
    canvas.create_image(75, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))

rates = [
    (0.5, 150),
    (1.0, 100),
    (2.0, 50),
    (4.0, 0),
]

def graphPageMousePressed(app, event):
    # hit back button
    if 50 < event.x < 100 and 30 < event.y < 70:
        app.page = AppPage.Options
        # reset group animation
        app.groupIdx = 1
        app.animate = False

    # click on visual rate
    for (idx, (x0, y0, x1, y1)) in enumerate(rateButtonPositions()):
        if x0 < event.x < x1 and y0 < event.y < y1:
            app.timerDelay = rates[idx][1]

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

def drawRegressionEquation(app, canvas):
    (points, xMin, xMax, yMin, yMax) = app.data.getScatterData(app.options.x, app.options.y)
    xList, yList = [], []

    for (px, py) in points:
        xList += [px]
        yList += [py]

    meanX = sum(xList)/len(xList)
    meanY = sum(yList)/len(yList)

    SSxx = 0
    SSxy = 0

    for idx in range(max(len(xList), len(yList))):
        SSxx += (xList[idx]-meanX)**2
        SSxy += (yList[idx]-meanY)*(xList[idx]-meanX)

    slope = round(SSxy/SSxx, 2)
    b = round(meanY - slope * meanX, 2)
    canvas.create_text(800, 200, text = f'{app.options.y} = {slope}*{app.options.x} + {b}', anchor = 'w', font = 'Arial 14')

def drawScatter(app, canvas):
    drawBackButton(app, canvas)
    (points, xMin, xMax, yMin, yMax) = app.data.getScatterData(app.options.x, app.options.y)
    pad = 40

    graphWidth = app.width - pad * 2
    widthRatio = graphWidth / (xMax - xMin)
    graphHeight = app.height - pad * 4
    heightRatio = graphHeight / (yMax - yMin)

    # x-axis
    canvas.create_line(pad, app.height - pad - graphHeight, pad, app.height - pad)
    canvas.create_text(app.width / 2, app.height - pad/2, text=app.options.x)
    # y-axis
    canvas.create_line(pad, app.height - pad, app.width - pad, app.height - pad)
    canvas.create_text(pad, app.height - pad - graphHeight - 20, text=app.options.y)

    for (px, py) in points:
        x = pad + (px - xMin) * widthRatio
        y = app.height - pad - (py - yMin) * heightRatio
        canvas.create_oval(x-2, y-2, x+2, y+2)

    canvas.create_text(app.width/2, 20, text=f'Scatterplot - {app.options.x}-{app.options.y}', font='Arial 16')

    # linear regression line
    xList, yList = [], []

    for (px, py) in points:
        x = pad + (px - xMin)*widthRatio
        y = app.height-pad-(py-yMin)*heightRatio
        xList += [x]
        yList += [y]

    meanX = sum(xList)/len(xList)
    meanY = sum(yList)/len(yList)

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
    canvas.create_text(app.width/2, 40, text=f'NBA {app.options.x}-{app.options.y} Linear Regression', font='Arial 10')

    drawRegressionEquation(app, canvas)

def drawBar(app, canvas):
    drawBackButton(app, canvas)
    aggregates = app.data.getAggregates(app.options.x, app.options.y)
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
        canvas.create_text(x1 + 20 , (y0 + y1) / 2, text=str(yvar), font='Arial 12')
        h += 60

    canvas.create_text(app.width/2, 20, text=f'Bar - {app.options.y} by {app.options.x}', font='Arial 16')

def drawGroups(app, canvas):
    drawBackButton(app, canvas)
    drawVisualRates(app, canvas)
    groups = app.data.getAggregatesGroups(app.options.x, app.options.y, app.options.group)
    idx = min(len(groups), app.groupIdx)
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
        canvas.create_text(x1 + 20 , (y0 + y1) / 2, text=str(yvar), font='Arial 12')
        h += 60

    canvas.create_text(app.width/2, 30, text=f'{app.options.y} by {app.options.x} over {app.options.group}', font='Arial 20')
    canvas.create_text(app.width/2, 55, text=f'(P to Start/Pause and S to Step)', font='Arial 12')
    canvas.create_text(280, 50, text=f'{app.options.group} : {group}', font='Arial 18', anchor='w')

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
