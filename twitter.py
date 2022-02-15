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

# TO READ THE CONVERSATIONS FROM PHOTOS
import requests
import io
from PIL import Image
# import easyocr
import os
from dotenv import load_dotenv
from pathlib import Path

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

SCREENNAME = "JobsMierda"
MOST_RECENT_ID = 0


class TwitterClient(object):

    def __init__(self):
        # To set your environment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'

        # En este caso no tengo access_token y access_key sino bearer_token, pues al estar usando una cuenta para academic research solo tengo OAuth 2.0 en vez de OAuth 1.0
        # bearer_token = 'XXXX'
        dotenv_path = Path('/home/kali/TwitterTokens.env')
        load_dotenv(dotenv_path=dotenv_path)

        consumer_key = os.getenv('API_KEY')
        consumer_secret = os.getenv('API_KEY_SECRET')

        try:
            # creamos el objeto AppAuthHandler
            self.auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

            # Creamos el objeto de API de tweepy para acceder a los tweets
            self.api = tweepy.API(self.auth)

        except:
            print("ERROR: NO SE HA PODIDO AUTENTICAR")

    def clean_text(self, text):

        clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
        clean_text = re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)", "", clean_text)
        clean_text = re.sub(r"https\S+", "", clean_text)
        return " ".join(clean_text.split())

    def get_images_from_tweet(self, tweet):
        images = set()

        if ('media' in tweet.entities):

            for image in tweet.extended_entities['media']:
                images.add(image['media_url'])

        return images



    def get_all_tweets_from_user(self, screen_name):



        # inicializamos una lista que contendra todos los tweets
        alltweets = []

        # primero buscamos los 200 primeros (tam max del count)
        new_tweets = self.api.search_tweets(q='from:' + screen_name + ' -filter:retweets', count=10, lang="es")

        # guardamos estos tweets en nuestro array de todos los tweets
        alltweets.extend(new_tweets)
        # seguiremos cogiendo tweets hasta que no queden

        #while len(new_tweets) > 0:
            # guardamos el id del ultimo tweet - 1
         #   oldest = alltweets[len(alltweets) - 1].id - 1

            # usamos el max_id para evitar que se cojan repetidos
          #  new_tweets = self.api.search_tweets(q='from:' + screen_name + ' -filter:retweets', count=200, max_id=oldest)
            # guardamos estos tweets en nuestro array de todos los tweets
           # alltweets.extend(new_tweets)

        return alltweets



    def get_useful_tweets_Afinn(self, screen_name):

        #afn = Afinn(language='es')
        tweets = self.get_all_tweets_from_user(screen_name)
        meaningful_tweets = []

        for tweet in tweets:
            text = self.clean_text(tweet.text)
            # print(text + " " + str(afn.score(text)))
            if len(text) > 0: #and afn.score(text) <= 0:
                meaningful_tweets.append(tweet)

        return meaningful_tweets

    def get_useful_tweets(self, screen_name):
        tweets = self.get_all_tweets_from_user(screen_name)
        meaningful_tweets = []
        # sentiment_classifier = SentimentClassifier()

        for tweet in tweets:
            if len(tweet.text) > 0:  # and sentiment_classifier.predict(tweet.text) <= 0.5:
                meaningful_tweets.append(tweet)

        return meaningful_tweets

    def retreive_info_tweet(self, tweet):
        link = "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)
        tweet_id = tweet.id
        user = tweet.user.screen_name
        date = tweet.created_at
        n_likes = tweet.favorite_count
        n_retweets = tweet.retweet_count

        n_replies = 0
        replies = self.api.search_tweets(q='to:'+user, since_id=tweet_id)

        for reply in replies:
            if reply.in_reply_to_status_id == tweet_id:
                n_replies += 1

        # fetching the status
        status = self.api.get_status(tweet_id, tweet_mode="extended")
        text = self.clean_text(status.full_text)

        dataset = pd.DataFrame(data={'link': [link], 'id': [tweet_id], 'text': [text], 'user': [user], 'date': [date], 'likes': [n_likes], 'retweets': [n_retweets], 'replies': [n_replies]})
        dataset['date'] = dataset['date'].dt.strftime('%d/%m/%y - %H:%M')
        json_object = dataset.to_json(force_ascii=False, orient='records').replace('\/', '/')
        #json_object = json.dumps(dataset)
        #json_object = json.loads(json_object)
        return json_object


def main():
    api = TwitterClient()
    tweets = api.get_useful_tweets_Afinn(screen_name=SCREENNAME)
    json_array = []
    for tweet in tweets:
        json_array.append(api.retreive_info_tweet(tweet))

    print('[')
    for json in json_array:
        print(json[1:-1])
    print(']')


    f = open("examples.json", 'a')
    f.write('[')
    for json in json_array:
        f.write(json[1:-1])
        f.write("\n")
    f.write(']')


if __name__ == "__main__":
    # calling main function
    main()
