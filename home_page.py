import os
from PIL import Image, ImageTk
from tkinter import filedialog

from data_manager import DataSet
from definitions import *

def drawHome(app, canvas):

    # learned how to use Image and ImageTk from:
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#loadImageUsingUrl
    canvas.create_image(400, 300, image=ImageTk.PhotoImage(app.imageManager.getImage('twitter')))
    canvas.create_image(750, 300, image=ImageTk.PhotoImage(app.imageManager.getImage('NBA')))
    canvas.create_image(app.width/2, 650, image=ImageTk.PhotoImage(app.imageManager.getImage('file')))

    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 75, text='WELCOME TO GRAPHOS!', font=font)
    canvas.create_text(app.width/2, 125, text='TRY OUT ONE OF OUR BUILT-IN DATASETS!', font=font)
    canvas.create_text(app.width/2, 500, text='OR INPUT YOUR OWN CSV FILE TO SEE SOME MAGIC', font=font)

    canvas.create_rectangle(500, 200, 625, 250, width=3)
    canvas.create_text(562, 225, text='  Livestream \n Twitter Data', font='22')
    canvas.create_rectangle(850, 200, 975, 250, width=3)
    canvas.create_text(912, 225, text='  View NBA \n    Data', font='22')

def homePageMousePressed(app, event):
    if 850 < event.x < 975 and 200 < event.y < 250:
        app.data = DataSet.load('nba_stats.csv')
        app.page = AppPage.Options
    elif 575 < event.x < 700 and 600 < event.y < 700:
        path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select data file: ',filetypes = (('csv file','*.csv'),('all files','*.*')))
        if path == '': 
            pass
        else:
            app.data = DataSet.load(path)
            app.page = AppPage.Options
            app.options = GraphOptions()
