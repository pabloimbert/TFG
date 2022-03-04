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





def clean_text(text):

    clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
    clean_text = re.sub("(@.+)|(#.+)•", "", clean_text)
    clean_text = re.sub(r"https\S+", "", clean_text)
    clean_text = re.sub(r'[^\w]', ' ', clean_text)
    clean_text = clean_text.lower()

    return " ".join(clean_text.split())

def getMedia():

    aux1 = pd.read_csv("../corpus/IMDB_Dataset_SPANISH.csv")
    aux2 = pd.read_csv("../corpus/punta_cana.csv")
    aux4 = pd.read_csv("../corpus/data_larazon_publico_v2.csv")
    text_IMDB = aux1['review_es']
    text_puntacana = aux2['review_text']
    text_larazon = aux4['cuerpo']
    avg_array = []
    i = 0

    for text in text_IMDB:
        if i == 152:
            break
        text = clean_text(text)
        text_len = len(text.split())
        avg_array.append(text_len)
        i+=1
    print("Average length IMDB ", statistics.mean(avg_array))
    print("Median length IMDB ", statistics.median(avg_array))

    avg_array = []
    i = 0

    for text in text_puntacana:
        if i == 152:
            break
        text = clean_text(text)
        text_len = len(text.split())
        avg_array.append(text_len)
        i += 1
    print("Average length puntacana ", statistics.mean(avg_array))
    print("Median length puntacana ", statistics.median(avg_array))


    avg_array = []
    i = 0

    for text in text_larazon:
        if i == 152:
            break
        text = clean_text(text)
        text_len = len(text.split())
        avg_array.append(text_len)
        i += 1
    print("Average length larazon ", statistics.mean(avg_array))
    print("Median length larazon ", statistics.median(avg_array))




    #user_id = self.cl.user_id_from_username(userName)
    #medias = self.cl.user_medias(user_id, 803)

    #captions = []
    #avg = 0
    #avg_array = []
    #lemmatized = []
    #every_word = ""
    #text = ""
    #irrelevant_posts = [31, 213, 386, 499, 631]
    #i = 0

    #for media in medias:
        #if i > 650:
            #media_caption = media.dict().get('caption_text')
            #media_caption=self.clean_text(media_caption)
            #text_len = len(media_caption.split())
            #avg_array.append(text_len)
            #captions.append(media_caption)

        #i = i + 1


    #column_names = ['Text','Prediction']
    #data=[]

    #for caption in captions:
        #data.append([caption,1])

    #training = pd.DataFrame(data, columns=column_names)
    #training.to_csv('../../text/training.csv')
    #print("Average length ",statistics.mean(avg_array))
    #print("Median length ",statistics.median(avg_array))



def main():
    getMedia()



if __name__ == "__main__":
    # calling main function
    main()

