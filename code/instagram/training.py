import datetime
import re
import csv
import stanza

# TO FILTER THE EMOJIS FROM THE TEXT
import emoji
import string

import pandas as pd

import keyring as kr
import instagrapi

from instagrapi import Client
import statistics
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
        credential =kr.get_credential("system", "mentalrevolutionfdi")
        self.cl.login(credential.username,credential.password)

    def clean_text(self, text):

        clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
        clean_text = re.sub("(@.+)|(#.+)•", "", clean_text)
        clean_text = re.sub(r"https\S+", "", clean_text)
        clean_text = re.sub(r'[^\w]', ' ', clean_text)
        clean_text = clean_text.lower()

        return " ".join(clean_text.split())

    def getMedia(self, userName):
        user_id = self.cl.user_id_from_username(userName)
        medias = self.cl.user_medias(user_id, 803)
        captions = []
        avg = 0
        avg_array = []
        lemmatized = []
        every_word = ""
        text = ""
        irrelevant_posts = [31, 213, 386, 499, 631]
        i = 0

        for media in medias:
            if i > 650:
                media_caption = media.dict().get('caption_text')
                media_caption=self.clean_text(media_caption)
                text_len = len(media_caption.split())
                avg_array.append(text_len)
                captions.append(media_caption)

            i = i + 1


        column_names = ['Text','Prediction']
        data=[]

        for caption in captions:
            data.append([caption,1])

        training = pd.DataFrame(data, columns=column_names)
        training.to_csv('../../text/training.csv')
        print("Average length ",statistics.mean(avg_array))
        print("Median length ",statistics.median(avg_array))



def main():
    cli = InstagramClient()
    cli.getMedia(USERNAME)



if __name__ == "__main__":
    # calling main function
    main()