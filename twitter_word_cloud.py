import os
import tweepy
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy


consumer_key = os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_SECRET_KEY')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_SECRET_TOKEN')

class TweepyStreamListener(tweepy.StreamListener):

    def __init__(self):
        super(TweepyStreamListener, self).__init__()
        self.counts = {}
        self.statusCounter = 0

    def on_status(self, status):
        #print(status.text)
        self.statusCounter += 1
        for token in status.text.split():
            if not token.startswith("#") or not token.isascii():
                continue

            if token not in self.counts:
                self.counts[token] = 0
            self.counts[token] += 1

    def on_error(self, status_code):
        print('tweepy error', status_code)
        # return False disconnects stream
        return False


class TwitterWordCloud:
    def __init__(self):
        self.listener = TweepyStreamListener()
        # learned how to use function OAuthHandler and setting tokens from
        # http://docs.tweepy.org/en/latest/auth_tutorial.html

        keysMissing = not all(
            [consumer_key, consumer_secret, access_token, access_token_secret]
        )
        if keysMissing:
            print("Missing Twitter Developer Keys!!!")
            self.stream = None
        else:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.stream = tweepy.Stream(auth, self.listener)
        self.lastWordCloud = None

    def run(self):
        # todo: cite acquaintance
        # stream data in a separate thread so main thread can draw
        # for filters, is_async from http://docs.tweepy.org/en/latest/streaming_how_to.html
        if self.stream:
            self.stream.sample(languages=['en'], is_async=True)

    def stop(self):
        if self.stream:
            self.stream.running = False

    def getWordCloud(self, width, height):
        if not self.stream or not self.listener.counts:
            return None

        if not self.stream.running:
            return self.lastWordCloud

        # twitter screenshot taken from https://www.nicepng.com/maxp/u2w7i1i1w7y3y3q8/
        outline = numpy.array(Image.open('images/tweety1.png'))
        wc = WordCloud(background_color='white', width=width, height=height,
                       mask=outline, contour_width=3, contour_color='lightblue', max_font_size=36, max_words=100)
        wc.generate_from_frequencies(self.listener.counts)
        twitter_colors = ImageColorGenerator(outline)
        wc.recolor(color_func=twitter_colors)

        self.lastWordCloud = wc
        return wc
