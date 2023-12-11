# post MVP file: generating a real-time hashtag twitter-shaped word cloud 
# uses Twitter's API tweety
import os
import tweepy
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy

# access keys: lines 9-12 source from acquaintance on keeping keys secret
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
        # http://docs.tweepy.org/en/latest/auth_tutorial.html lines 41, 52-54

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
        # acquaintance helped with line 62 (no credit)
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

        # twitter image taken from https://similarpng.com/gradient-logo-twitter-png/
        # by Alikae Andro, but self edited aqnd screenshotted
        # next few lines, found the parameters for creating wordcloud from:
        # https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
        # inspired to create the gradient colored text from example 3 in:
        # https://medium.com/better-programming/create-custom-word-clouds-in-python-841563933e73

        outline = numpy.array(Image.open('images/tweety1.png'))
        wc = WordCloud(background_color='white', width=width, height=height,
                       mask=outline, contour_width=3, contour_color='lightblue', max_font_size=36, max_words=100)
        wc.generate_from_frequencies(self.listener.counts)
        twitter_colors = ImageColorGenerator(outline)
        wc.recolor(color_func=twitter_colors)

        self.lastWordCloud = wc
        return wc
