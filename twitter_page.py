from PIL import ImageTk

def drawTwitter(app, canvas):
    try:
        canvas.create_text(app.width/2, 20, text='TWITTER', font='Arial 20')

        wc = app.data.getWordCloud(800, 600)
        if not wc:
            return

        x = wc.to_image()
        canvas.create_image(100, 100, image=ImageTk.PhotoImage(x), anchor='nw')
    except:
        app.data.stop()

