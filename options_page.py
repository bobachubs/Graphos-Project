from common import *
from PIL import Image, ImageTk

modes = [
    ('Histogram', GraphMode.Histogram),
    ('Scatterplot', GraphMode.Scatter),
    ('Bar', GraphMode.Bar),
    ('Bar Groups', GraphMode.Groups),
]

scatterRangeAttributes = ['xMin', 'xMax', 'yMin', 'yMax']

def modeButtonPositions():
    positions = []

    x = 120
    y = 140
    boxWidth = 400
    boxHeight = 40
    for _ in modes:
        positions.append((x, y, x + boxWidth, y + boxHeight))
        y += boxHeight
    return positions

def xVariableButtonPositions(fieldStrings):
    positionsX = []

    x = 80
    y = 350
    boxWidth = 150
    boxHeight = 40
    for xVar in fieldStrings:
        positionsX.append((x + boxWidth/2, y-boxHeight/2, x + 3*boxWidth/2, y + boxHeight/2))
        y += boxHeight

    return positionsX

def yVariableButtonPositions(fieldStrings):
    positionsY = []

    x = 400
    y = 350
    boxWidth = 150
    boxHeight = 40
    for yVar in fieldStrings:
        positionsY.append((x + boxWidth/2, y-boxHeight/2, x + 3*boxWidth/2, y + boxHeight/2))
        y += boxHeight

    return positionsY

def groupButtonPositions(fieldStrings):
    positionsG = []

    x = 720
    y = 350
    boxWidth = 150
    boxHeight = 40
    for yVar in fieldStrings:
        positionsG.append((x + boxWidth/2, y-boxHeight/2, x + 3*boxWidth/2, y + boxHeight/2))
        y += boxHeight

    return positionsG

def scatterRangeButtonPositions():
    positionsR = []

    x = 800
    y = 350
    boxWidth = 150
    boxHeight = 40
    for value in scatterRangeAttributes:
        positionsR.append((x + boxWidth/2, y-boxHeight/2, x + 3*boxWidth/2, y + boxHeight/2))
        y += boxHeight

    return positionsR

def optionsPageMousePressed(app, event):
    # back button
    if 50 < event.x < 100 and 30 < event.y < 70:
        app.page = AppPage.Home
        return

    # go button
    if 1180 < event.x < 1230 and 730 < event.y < 770:
      if app.options.mode == GraphMode.Histogram:
          if app.options.x != None:
              app.page = AppPage.Graph
      elif app.options.mode == GraphMode.Groups:
          if all((var is not None for var in [app.options.x, app.options.y, app.options.group])):
              app.page = AppPage.Graph
      else:
          if app.options.x != None and app.options.y != None:
              app.page = AppPage.Graph

    # mode selection
    for (idx, (x0, y0, x1, y1)) in enumerate(modeButtonPositions()):
        if x0 < event.x < x1 and y0 < event.y < y1:
            newOptions = GraphOptions()
            newOptions.mode = modes[idx][1]
            app.options = newOptions
            break

    # x-variable selection
    if app.options.mode in [GraphMode.Histogram, GraphMode.Scatter]:
        xVariables = [f.name for f in app.data.fields if f.isNumeric]
    else:
        xVariables = [f.name for f in app.data.fields if not f.isNumeric]
    positionsX = xVariableButtonPositions(xVariables)
    for (idx, (x0, y0, x1, y1)) in enumerate(positionsX):
        if x0 < event.x < x1 and y0 < event.y < y1:
            app.options.x = xVariables[idx]
            break

    # y-variable selection
    if app.options.mode != GraphMode.Histogram:
        yVariables = [f.name for f in app.data.fields if f.isNumeric]
        positionsY = yVariableButtonPositions(yVariables)
        for (idx, (x0, y0, x1, y1)) in enumerate(positionsY):
            if x0 < event.x < x1 and y0 < event.y < y1:
                app.options.y = yVariables[idx]
                break

    # group selection
    if app.options.mode == GraphMode.Groups:
        gVariables = [f.name for f in app.data.fields if f.name.lower() in ['time', 'date']]
        positionsG = groupButtonPositions(gVariables)
        for (idx, (x0, y0, x1, y1)) in enumerate(positionsG):
            if x0 < event.x < x1 and y0 < event.y < y1:
                app.options.group = gVariables[idx]
                break

    # scatter range selection
    if app.options.mode == GraphMode.Scatter:
        positionsR = scatterRangeButtonPositions()
        for (idx, (x0, y0, x1, y1)) in enumerate(positionsR):
            attribute = scatterRangeAttributes[idx]
            if x0 < event.x < x1 and y0 < event.y < y1:
                try:
                    inputValue = float(app.getUserInput(attribute))
                except:
                    inputValue = None
                setattr(app.options, attribute, inputValue)
                break

def drawOptions(app, canvas):
    canvas.create_image(75, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))
    if app.options.mode:
        canvas.create_image(1205, 750, image=ImageTk.PhotoImage(app.imageManager.getImage('go')))

    # Modes
    canvas.create_text(80, 100, text='Graph Mode', font='Arial 22 bold', anchor='w')

    for (idx, (x0, y0, x1, y1)) in enumerate(modeButtonPositions()):
        buttonHeight = y1 - y0
        r = buttonHeight / 4
        mode = modes[idx][1]
        canvas.create_oval(x0, y0 - r, x0 + r * 2, y0 + r, fill='black' if app.options.mode == mode else None)
        modeString = modes[idx][0]
        canvas.create_text(x0 + r * 3, y0, text=modeString, font='Arial 18', anchor='w')

    if not app.options.mode:
        return

    # x-variable
    canvas.create_text(80, 300, text='X-Var', font='Arial 22 bold', anchor='w')

    if app.options.mode in [GraphMode.Histogram, GraphMode.Scatter]:
        # histogram and scatterplot variable must be numeric
        xVariables = [f.name for f in app.data.fields if f.isNumeric]
    else:
        xVariables = [f.name for f in app.data.fields if not f.isNumeric]

    positionsX = xVariableButtonPositions(xVariables)
    for (idx, (x0, y0, x1, y1)) in enumerate(positionsX):
        xVar = xVariables[idx]
        canvas.create_rectangle(x0, y0, x1, y1, fill='black' if app.options.x == xVar else None)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=xVar, fill='white' if app.options.x == xVar else 'black')
    
    # histogram only takes one variable
    if app.options.mode == GraphMode.Histogram:
        return

    # y-variable
    canvas.create_text(400, 300, text='Y-Var', font='Arial 22 bold', anchor='w')

    yVariables = [f.name for f in app.data.fields if f.isNumeric]

    positionsY = yVariableButtonPositions(yVariables)
    for (idx, (x0, y0, x1, y1)) in enumerate(positionsY):
        yVar = yVariables[idx]
        canvas.create_rectangle(x0, y0, x1, y1, fill='black' if app.options.y == yVar else None)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=yVar, fill='white' if app.options.y == yVar else 'black')

    # group option
    if app.options.mode == GraphMode.Groups:
        canvas.create_text(720, 300, text='Group', font='Arial 22 bold', anchor='w')

        gVariables = [f.name for f in app.data.fields if f.name.lower() in ['time', 'date']]

        positionsG = groupButtonPositions(gVariables)
        for (idx, (x0, y0, x1, y1)) in enumerate(positionsG):
            gVar = gVariables[idx]
            canvas.create_rectangle(x0, y0, x1, y1, fill='black' if app.options.group == gVar else None)
            canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=gVar, fill='white' if app.options.group == gVar else 'black')

    # scatter range option
    if app.options.mode == GraphMode.Scatter:
        canvas.create_text(720, 300, text='Y-Range', font='Arial 22 bold', anchor='w')
        positionsR = scatterRangeButtonPositions()
        for (idx, (x0, y0, x1, y1)) in enumerate(positionsR):
            attribute = scatterRangeAttributes[idx]
            canvas.create_rectangle(x0, y0, x1, y1)
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text=f'{attribute}={getattr(app.options, attribute)}')
