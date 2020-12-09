import os
from PIL import Image, ImageTk

from data_manager import DataSet
from definitions import *

def drawBackButton(app, canvas):
    canvas.create_image(75, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))

def infoPageMousePressed(app, event):
    if 50 < event.x < 100 and 30 < event.y < 70:
        app.page = AppPage.Home

def drawInfo(app, canvas):
    drawBackButton(app, canvas)

    font = 'Arial 20'
    canvas.create_text(app.width/2, 60, text='INFORMATION PAGE!', font='Arial 30 bold')
    canvas.create_text(90, 130, text='Welcome to Graphos! Graphos is a basic, general purpose visualizer which allows users to input a csv file and', font=font, anchor ='w')
    canvas.create_text(90, 160, text ='select the variables they want to graph in a Scatterplot, Histogram, Bar Graph, or Animated Bar Graph by Group', font=font, anchor ='w')
    canvas.create_text(90, 220, text='To get started, go to the Graphos home page and explore our features using our built-in NBA dataset', font=font, anchor ='w')
    canvas.create_text(90, 280, text = 'Or, click on the Twitter box and hit the space bar to view a word cloud of current, trendy Twitter hashtags', font=font, anchor ='w')
    canvas.create_text(90, 340, text = 'Note: to view the Animated Bar Graph by Time (Group), the inputted csv file date column must be in the format #### - ## - ##', font=font, anchor ='w')