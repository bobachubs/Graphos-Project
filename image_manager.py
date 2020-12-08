
class ImageManager:
    def __init__(self):
        self.cache = {}

    @staticmethod
    def load(app):
        imageManager = ImageManager()

        # imagelArrow and imageArrowGo:
        # https://material.io/resources/icons/?icon=double_arrow&style=twotone
        # imageTwitter:
        # https://assets.stickpng.com/images/580b57fcd9996e24bc43c53e.png
        # imageNBA
        # https://cdn.freebiesupply.com/images/large/2x/nba-logo-transparent.png
        # imageFile
        # https://material.io/resources/icons/?icon=folder_open&style=baseline
        # loading image idea from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#loadImageUsingUrl
        
        imageArrow = app.scaleImage(app.loadImage('images/arrow.png'), 1)
        imageArrowGo = app.scaleImage(app.loadImage('images/go.png'), 1)
        imageTwitter = app.scaleImage(app.loadImage('images/twitter.png'), 1)
        imageNBA = app.scaleImage(app.loadImage('images/nba.png'), 1)
        imageFile = app.scaleImage(app.loadImage('images/file.png'), 1)

        imageManager.cache['arrow'] = imageArrow
        imageManager.cache['go'] = imageArrowGo
        imageManager.cache['twitter'] = imageTwitter
        imageManager.cache['NBA'] = imageNBA
        imageManager.cache['file'] = imageFile

        return imageManager

    def getImage(self, key):
        return self.cache.get(key)
