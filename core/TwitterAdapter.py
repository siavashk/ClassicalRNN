import os
import tweepy

class TwitterAdapter(object):
    def __init__(self, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
        consumer_key           = os.environ['CONSUMER_KEY']           if consumer_key is None else consumer_key
        consumer_secret        = os.environ['CONSUMER_SECRET']        if consumer_key is None else consumer_secret
        access_token           = os.environ['ACCESS_TOKEN']           if access_token is None else access_token
        access_token_secret    = os.environ['ACCESS_TOKEN_SECRET']    if access_token is None else access_token_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.published = False

    def updateStatus(self):
        if not self.published:
            self.api.update_status('First tweet!')
