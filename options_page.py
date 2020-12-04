from common import *
from PIL import Image, ImageTk

relevantFields = ['FGA', 'PTS', 'AST', 'PLUS_MINUS']

def drawBackButtonHome(app, canvas):
    canvas.create_image(75, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))

def xVariableButtonPositions(xVariables):
    positions = []

    x = 350
    y = 500
    boxWidth = 100
    boxHeight = 50
    for xVar in xVariables:
        positions.append((x - boxWidth/2, y-boxHeight/2, x + boxWidth/2, y + boxHeight/2))
        y += boxHeight

    return positions

def optionsPageMousePressed(app, event):
    if 50 < event.x < 100 and 30 < event.y < 70:
        app.page = AppPage.Home
        return
    elif 200 < event.y < 250:
        app.options.mode = GraphMode.Histogram
        app.options.x = None
        app.options.y = None
    elif 250 < event.y < 300:
        app.options.mode = GraphMode.Scatter
        app.options.x = None
        app.options.y = None
    elif 300 < event.y < 350:
        app.options.mode = GraphMode.Bar

    for (idx, (x0, y0, x1, y1)) in enumerate(xVariableButtonPositions(relevantFields)):
        if x0 < event.x < x1 and y0 < event.y < y1:
            app.options.x = relevantFields[idx]
            break

    ### hacky
    if app.options.mode == GraphMode.Histogram and app.options.x != None:
        app.page = AppPage.Graph

def drawOptions(app, canvas):
    drawBackButtonHome(app, canvas)
    modes = [
        ('HISTOGRAM', GraphMode.Histogram),
        ('SCATTERPLOT', GraphMode.Scatter),
        ('BAR', GraphMode.Bar),
    ]

    x = 225
    y = 200
    r = 10
    for (modeString, mode) in modes:
        canvas.create_text(x, y, text=modeString, font='Arial 26 bold', anchor='nw')
        canvas.create_oval(x-r-50, y-r+10, x+r-40, y+r+20, fill='black' if app.options.mode == mode else None) 
        y += 50

    if not app.options.mode:
        return

    positions = xVariableButtonPositions(relevantFields)
    for (idx, (x0, y0, x1, y1)) in enumerate(positions):
        xVar = relevantFields[idx]
        canvas.create_rectangle(x0, y0, x1, y1, fill='black' if app.options.x == xVar else None)
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=xVar, fill='white' if app.options.x == xVar else 'black')

def drawHeaders(app, canvas):
    # draw titles and headings
    canvas.create_text(app.width/2, 50, text='PICK YOUR DISPLAY', font='Arial 34 bold')
    canvas.create_text(80, 120, text='VISUALIZATION MODE', font='Arial 26 bold', anchor='nw')
    canvas.create_text(80, 380, text='SELECT YOUR VARIABLES', font='Arial 24 bold', anchor = 'nw')
    canvas.create_text(210, 550, text='X: ', font='Arial 100')
    canvas.create_text(550, 550, text='Y: ', font='Arial 100')
'''
class OptionsMenuMode(Mode):
    def appStarted(mode):
        mode.selectVar = False
        mode.numModes = 4
        mode.visualModeCir = []
        mode.variableXCoor = []
        mode.variableYCoor = []
        mode.visualOptions = ['Scatterplot', 'Bar', 'Histogram', 'Time']
        mode.visualOptionBools = [False, False, False, False]
        mode.visualOption = None
        mode.variableOption = None
        mode.fill = None
        mode.x_var = False
        mode.y_var = False
        mode.graphX = ['Time','Age', 'Years']
        mode.graphY = ['Points','Age']
        mode.graphVarX = None
        mode.graphVarY = None

    # https://www.cs.cmu.edu/~112/notes/notes-oop-part1.html


    def drawVisualModes(mode, canvas):
        canvas.create_text(225, 200, text='SCATTERPLOT (W/ LINEAR REGRESSION)', font='Arial 22 bold', anchor='nw')
        canvas.create_text(225, 250, text='BAR CHART (W/ PIE CHART)', font='Arial 22 bold', anchor='nw')
        canvas.create_text(225, 300, text='HISTOGRAM', font='Arial 22 bold', anchor='nw')
        canvas.create_text(225, 350, text='TIME ANIMATION', font='Arial 22 bold', anchor='nw')
        r = 15
        y = 212
        for visual in range(mode.numModes):       
            if len(mode.visualModeCir) < 4:
                mode.visualModeCir.append((167, y))
            y += 50

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width/2, 50, text='PICK YOUR DISPLAY', font='Arial 34 bold')
        canvas.create_text(225, 150, text='VISUALIZATION MODE', font='Arial 26 bold')
        if True in mode.visualOptionBools: 
            idx1 = mode.visualOptionBools.index(True)
        else:
            idx1 = None
        for idx in range(len(mode.visualModeCir)):
            r = 15
            x,y = mode.visualModeCir[idx][0], mode.visualModeCir[idx][1]
            if idx == idx1: mode.fill = 'black'
            else: mode.fill = None
            canvas.create_oval(x-r, y-r, x+r, y+r, fill = mode.fill)

        mode.drawVisualModes(canvas)
        if mode.selectVar == True:
                canvas.create_text(225, 450, text='SELECT YOUR VARIABLES', font='Arial 24 bold')

        if mode.selectVar == True and (mode.x_var, mode.y_var) == (True, True): 
            canvas.create_text(210, 600, text='X: ', font='Arial 50 bold')
            canvas.create_text(500, 600, text='Y: ', font='Arial 50 bold')
            mode.drawVariables(canvas, 'x', mode.graphX)
            mode.drawVariables(canvas, 'y', mode.graphY)
        elif mode.selectVar == True and (mode.x_var, mode.y_var) == (True, False):
            canvas.create_text(210, 600, text='X: ', font='Arial 50 bold')
            mode.drawVariables(canvas, 'x', mode.graphX)

    def drawVariables(mode, canvas, x_y, List):
        if x_y == 'x':
            startX, startY = 250, 500
        elif x_y == 'y':
            startX, startY = 550, 500
        # 250, 500, 720, 750
        # 550, 500, 720, 750
        pad = 10
        numBox = len(List)
        width = len(mode.graphX)
        widthBox = 200//width - pad
        for var in range(numBox):
            canvas.create_rectangle(startX, startY, startX + 170, startY + widthBox)
            textX = (2*startX + 170)/2
            textY = (2*startY + widthBox)/2
            if len(mode.variableXCoor) <= len(mode.graphX):
                mode.variableXCoor.append((textX, textY))
            else:
                mode.variableYCoor.append((textX, textY))
            canvas.create_text(textX, textY, text = List[var], font = "Arial 16")
            startY += widthBox + pad

    def mousePressed(mode, event):
        print(event.x, event.y)
        mode.checkVisualMode(event.x, event.y)
        # mode.checkVariableMode(event.x, event.y)
        print(mode.visualOption)
        print(mode.graphVarX, mode.graphVarY)
        print(mode.variableXCoor, mode.variableYCoor)

    def checkVariableMode(mode, x, y):
        for idx in range(len(mode.variableXCoor)):
            x1 = mode.variableXCoor[idx][0]
            y1 = mode.variableXCoor[idx][1]
            if x1-85 < x < x1+85 and y1-18 < y < y1+18:
                mode.graphVarX = mode.graphX[idx]

        for idx in range(len(mode.variableYCoor)):
            x1 = mode.variableYCoor[idx][0]
            y1 = mode.variableYCoor[idx][1]    
            if x1-85 < x < x1+85 and y1-18 < y < y1+18:
                mode.graphVarY = mode.graphY[idx]

    def checkVisualMode(mode, x, y):
        for idx in range(len(mode.visualOptions)):
            x1 = mode.visualModeCir[idx][0]
            y1 = mode.visualModeCir[idx][1]
            if  x1-15 < x < x1+15 and y1-15 < y < y1+15:
                mode.visualOption = mode.visualOptions[idx]
                if mode.selectVar == False:
                     mode.selectVar = True
                for idx1 in range(len(mode.visualOptionBools)):
                    if idx1 == idx: mode.visualOptionBools[idx1] = True
                    else: mode.visualOptionBools[idx1] = False

        if mode.visualOption == 'Scatterplot' or mode.visualOption == 'Bar':
            mode.x_var, mode.y_var = True, True
        elif mode.visualOption == 'Histogram' or mode.visualOption == 'Time':
            mode.x_var, mode.y_var = True, False
'''
