import datetime
import re

# TO CONVERT THE INFO TO A JSON
import json
# TO COLLECT THE TWEETS
import tweepy
import ujson as ujson
from tweepy import AppAuthHandler

# TO FILTER THE EMOJIS FROM THE TEXT
import emoji

# FOR THE SENTIMENT ANALYSIS
# from classifier import *
from afinn import Afinn

# from textblob import TextBlob
import numpy as np
import pandas as pd
# import nltk
# from nltk.stem import WordNetLemmatizer
import ssl

# from googletrans import Translator

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# ----------------------------------------------------     FIXED VALUES     --------------------------------------------------------------

SCREENNAME = "PabloImbert"
MOST_RECENT_ID = 0


class TwitterClient(object):

    def __init__(self):
        # To set your environment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'

        # En este caso no tengo access_token y access_key sino bearer_token, pues al estar usando una cuenta para academic research solo tengo OAuth 2.0 en vez de OAuth 1.0
        # bearer_token = 'XXXX'
        consumer_key = 'XXXX'
        consumer_secret = 'XXXX'

        try:
            # creamos el objeto AppAuthHandler
            self.auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

            # Creamos el objeto de API de tweepy para acceder a los tweets
            self.api = tweepy.API(self.auth)

        except:
            print("ERROR: NO SE HA PODIDO AUTENTICAR")


    def get_all_tweets_from_user(self):
            # inicializamos una lista que contendra todos los tweets
            alltweets = []

            # primero buscamos los 200 primeros (tam max del count)
            new_tweets = self.api.search_tweets(q="-filter:media -filter:retweets -filter:quote -filter:replies", count=153, lang="es")

            # guardamos estos tweets en nuestro array de todos los tweets
            alltweets.extend(new_tweets)

            return alltweets



    def get_useful_tweets(self):
        tweets = self.get_all_tweets_from_user()
        meaningful_tweets = []
        # sentiment_classifier = SentimentClassifier()

        for tweet in tweets:
            if len(tweet.text) > 0:  # and sentiment_classifier.predict(tweet.text) <= 0.5:
                status = self.api.get_status(tweet.id, tweet_mode="extended")
                text = status.full_text
                link = "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)
                print(link)
                meaningful_tweets.append(text)

        return meaningful_tweets


def main():
    api = TwitterClient()
    tweets = api.get_useful_tweets()
    f = open("random_tweets.txt", 'w')
    for tweet in tweets:
        f.write(tweet)
        f.write("#$%")



if __name__ == "__main__":
    # calling main function
    main()
