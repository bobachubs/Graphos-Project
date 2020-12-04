from PIL import Image, ImageTk
from common import *

def drawBackButton(app, canvas):
    canvas.create_image(75, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))

def graphPageMousePressed(app, event):
    if 50 < event.x < 100 and 30 < event.y < 70:
        app.page = AppPage.Options

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

    canvas.create_text(app.width/2, 20, text=f'NBA {app.options.x} Histogram', font='Arial 16')

def drawScatter(app, canvas):
    drawBackButton(app, canvas)
    (points, xMin, xMax, yMin, yMax) = app.data.getScatterData('FGA', 'PTS')
    pad = 40

    graphWidth = app.width - pad * 2
    widthRatio = graphWidth / (xMax - xMin)
    graphHeight = app.height - pad * 4
    heightRatio = graphHeight / (yMax - yMin)

    # x-axis
    canvas.create_line(pad, app.height - pad - graphHeight, pad, app.height - pad)
    canvas.create_text(app.width / 2, app.height - pad/2, text='FGA')
    # y-axis
    canvas.create_line(pad, app.height - pad, app.width - pad, app.height - pad)
    canvas.create_text(pad, app.height - pad - graphHeight - 20, text='PTS')

    for (px, py) in points:
        x = pad + (px - xMin) * widthRatio
        y = app.height - pad - (py - yMin) * heightRatio
        canvas.create_oval(x-2, y-2, x+2, y+2)

    canvas.create_text(app.width/2, 20, text=f'NBA FGA-PTS Scatterplot', font='Arial 16')

def drawBar(app, canvas):
    drawBackButton(app, canvas)
    #playerPoints = app.data.nbaPlayerPoints()
    playerPoints = app.data.getAggregates('PLAYER_NAME', 'PTS')
    pointLeaders = sorted(playerPoints.items(), key=lambda p: p[1], reverse=True)[:10]

    # Draw rectangles from the left proportional to the target ratio
    fullWidth = app.width - 40
    topStat = pointLeaders[0][1]
    ratio = fullWidth / topStat * 0.8

    h = 100
    for (player, points) in pointLeaders:
        x0 = 20
        y0 = h
        x1 = 20 + points * ratio
        y1 = h + 50
        color = app.colorManager.getColor(player)

        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=player, font='Arial 12')
        canvas.create_text(x1 + 20 , (y0 + y1) / 2, text=str(points), font='Arial 12')
        h += 60

    canvas.create_text(app.width/2, 20, text=f'NBA Point Leaders', font='Arial 16')

def drawTimeline(app, canvas):
    #playerPoints = app.data.nbaPlayerPoints()
    timeline = app.data.getAggregatesTimeline('PLAYER_NAME', 'PTS')
    idx = min(len(timeline), app.counter)
    (time, aggregates) = timeline[idx]
    pointLeaders = sorted(aggregates.items(), key=lambda p: p[1], reverse=True)[:10]

    # Draw rectangles from the left proportional to the target ratio
    fullWidth = app.width - 40
    topStat = pointLeaders[0][1]
    ratio = fullWidth / topStat * 0.8

    h = 100
    for (player, points) in pointLeaders:
        x0 = 20
        y0 = h
        x1 = 20 + points * ratio
        y1 = h + 50
        color = app.colorManager.getColor(player)

        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=player, font='Arial 12')
        canvas.create_text(x1 + 20 , (y0 + y1) / 2, text=str(points), font='Arial 12')
        h += 60

    canvas.create_text(app.width/2, 20, text=f'NBA Point Leaders Timeline', font='Arial 16')
    canvas.create_text(40, 40, text=time, font='Arial 14')
