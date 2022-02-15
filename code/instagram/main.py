import datetime
import re
import csv
import stanza
#stanza.download('es')
from django.conf import settings

settings.configure()

# TO FILTER THE EMOJIS FROM THE TEXT
import emoji


# FOR THE SENTIMENT ANALYSIS
# from classifier import *
#from afinn import Afinn
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
        self.cl.login('mentalrevolutionfdi', 'XXXXX')

    def getMedia(self, userName):
        user_id = self.cl.user_id_from_username(userName)
        medias = self.cl.user_medias(user_id, 10)
        captions = []
        lemmatized = []
        every_word = ""
        text = ""
        irrelevant_posts = [31, 213, 386, 499, 631]
        i = 0

        for media in medias:
            if i not in irrelevant_posts:
                media_caption = media.dict().get('caption_text')
                captions.append(media_caption)
                every_word = every_word + " " + media_caption
            i = i + 1


        nlp = spacy.load("es_core_news_sm")
        obj = nlp(every_word)
        tokens = [tk.orth_ for tk in obj if not tk.is_punct | tk.is_stop]
        normalized = [tk.lower() for tk in tokens if len(tk) > 3 and tk.isalpha()]

        for n in normalized:
            text = text + n + " "

        #stanza.download('es')
        nlp = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')
        doc = nlp(text)

        for sent in doc.sentences:
            for word in sent.words:
                lemmatized.append(word.lemma)

        freq = Counter(lemmatized).most_common()
        print(freq)

        #PARA ALMACENARLO EN UN CSV
        #with open('FREQUENCIES.csv', 'w') as f:
         #   csv_f = csv.writer(f)
         #   csv_f.writerow(['WORD', 'FREQUENCY'])
          #  for tuple in freq:
          #      csv_f.writerow(tuple)





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
