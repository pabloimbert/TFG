import datetime
import re
import csv
import stanza

# TO FILTER THE EMOJIS FROM THE TEXT
import emoji


# FOR THE SENTIMENT ANALYSIS
# from classifier import *
from afinn import Afinn
from instagrapi import Client
from collections import Counter
import spacy
import nltk
import nltk.data
from nltk import SnowballStemmer
# ----------------------------------------------------     FIXED VALUES     --------------------------------------------------------------

USERNAME = 'trabajosruineros'

class InstagramClient(object):
    def __init__(self):
        self.cl = Client()
        self.cl.login('mentalrevolutionfdi', 'XXXXXX')

    def getMedia(self, userName):
        user_id = self.cl.user_id_from_username(userName)
        medias = self.cl.user_medias(user_id, 803)
        captions = []
        lemmatized = []
        every_word = ""
        text = ""
        irrelevant_posts = [31, 213, 386, 499, 631]
        i = 0

        for media in medias:
            if i > 650:
                media_caption = media.dict().get('caption_text')
                captions.append(media_caption)
            i = i + 1

        f = open("../../text/training.txt", 'w')
        for caption in captions:
            f.write(caption)
            f.write("#$%")
            







def main():
    #api = TwitterClient()
    #tweets = api.get_useful_tweets_Afinn(screen_name=SCREENNAME)
    #dataset = 5
    #for tweet in tweets:
    #print(api.retreive_info_tweet(tweet, dataset))
    cli = InstagramClient()
    cli.getMedia(USERNAME)



if __name__ == "__main__":
    # calling main function
    main()