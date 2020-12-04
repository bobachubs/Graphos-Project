
class ImageManager:
    def __init__(self):
        self.cache = {}

    @staticmethod
    def load(app):
        imageManager = ImageManager()

        # urlArrow from https://material.io/resources/icons/?icon=double_arrow&style=twotone
        # urlTwitter from https://assets.stickpng.com/images/580b57fcd9996e24bc43c53e.png
        # urlNBA from https://cdn.freebiesupply.com/images/large/2x/nba-logo-transparent.png
        # urlFile from https://material.io/resources/icons/?icon=folder_open&style=baseline
        

        imageArrow = app.scaleImage(app.loadImage('images/arrow.png'), 1)
        imageTwitter = app.scaleImage(app.loadImage('images/twitter.png'), 1)
        imageNBA = app.scaleImage(app.loadImage('images/nba.png'), 1)
        imageFile = app.scaleImage(app.loadImage('images/file.png'), 1)

        imageManager.cache['arrow'] = imageArrow
        imageManager.cache['twitter'] = imageTwitter
        imageManager.cache['NBA'] = imageNBA
        imageManager.cache['file'] = imageFile

        return imageManager
    
    def getImage(self, key):
        return self.cache.get(key)


# def drawBackButton(app, canvas):
#     canvas.create_image(50, 50, image=ImageTk.PhotoImage(app.imageManager.getImage('arrow')))

        # if 1205 < event.x < 1235 and 735 < event.y < 765:
        #     mode.app.setActiveMode(mode.app.optionsMenuMode)