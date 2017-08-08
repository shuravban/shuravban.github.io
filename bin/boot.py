from twitter_keys import *

import tweepy

_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
_auth.set_access_token(access_token, access_secret)

api = tweepy.API(_auth)
