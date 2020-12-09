from PIL import ImageTk, Image
from definitions import *

def drawTitle(app, canvas):
    canvas.create_text(app.width/2, 25, text='TWITTER', font='Arial 24 bold', fill = 'royalblue')
    canvas.create_text(app.width/2, 55, text='(Space to Start/Pause)', font='Arial 12', fill = 'royalblue')    

def drawBackButton(app, canvas):
    canvas.create_image(75, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))

def twitterPageMousePressed(app, event):
    if 50 < event.x < 100 and 30 < event.y < 70:
        app.page = AppPage.Home
        app.data.stop()

def drawTwitter(app, canvas):
    drawBackButton(app, canvas)
    if not app.data.stream:
        canvas.create_text(app.width/2, app.height/2, text='MISSING TWITTER KEYS', font='Arial 24 bold', fill='red')
        drawTitle(app, canvas)
        return

    wc = app.data.getWordCloud(800, 600)
    if not wc:
        drawTitle(app, canvas)
        return

    x = wc.to_image()
    canvas.create_image(app.width/2, app.height/2 + 20, image=ImageTk.PhotoImage(x))
    # draw last so it's on top
    drawTitle(app, canvas)
