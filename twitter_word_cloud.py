import os
import tweepy
from wordcloud import WordCloud

consumer_key = os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_SECRET_KEY')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_SECRET_TOKEN')

class TweepyStreamListener(tweepy.StreamListener):

    def __init__(self):
        super(TweepyStreamListener, self).__init__()
        self.counts = {}

    def on_status(self, status):
        #print(status.text)
        for token in status.text.split():
            if not token.startswith("#"):
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
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = tweepy.Stream(auth, self.listener)

    def run(self):
        # todo: cite acquaintance
        # stream data in a separate thread so main thread can draw
        self.stream.sample(languages=['en'], is_async=True)

    def stop(self):
        self.stream.running = False

    def getWordCloud(self, width, height):
        if not self.listener.counts:
            return None

        wc = WordCloud(background_color='white', width=width, height=height)
        wc.generate_from_frequencies(self.listener.counts)
        return wc
