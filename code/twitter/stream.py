import re
import tweepy
import emoji
import os
import time

#from bson import ObjectId
from dotenv import load_dotenv , find_dotenv
from pymongo import MongoClient
import ssl
import pandas as pd
import spacy
import stanza


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# ----------------------------------------------------     FIXED VALUES     --------------------------------------------------------------

SCREENNAME = "JobsMierda"
MOST_RECENT_ID = 0


# set up a new class using tweepy.StreamListener

class SimpleListener(tweepy.Stream):
    client = MongoClient()
    db = client['tweet_stream']
    collection = db['test']

    def on_status(self, status):

        tweet_id = status.id_str


        #if hasattr(status, "retweeted_status"):  # Check if Retweet
        #    try:
        #        text = status.retweeted_status.extended_tweet['full_text']
        #        l_hashtags = status.retweeted_status.extended_tweet['entities']['hashtags']
        #    except AttributeError:
        #        text = status.retweeted_status.text
        #         l_hashtags = status.retweeted_status.entities['hashtags']
        #else:
        if not hasattr(status, "retweeted_status"):  # Check if not Retweet
            try:
                text = status.extended_tweet["full_text"]
                l_hashtags = status.extended_tweet['entities']['hashtags']
            except AttributeError:
                text = status.text
                l_hashtags = status.entities['hashtags']

            text.replace("\n", " ")
            user = status.user.screen_name
            link = "https://twitter.com/" + user + "/status/" + tweet_id

            date = status.created_at
            n_likes = status.favorite_count
            n_retweets = status.retweet_count
            n_replies = status.reply_count


            post = {'link': link, 'id': tweet_id, 'text': text, 'user': user, 'date': date, 'likes': n_likes,
            'retweets': n_retweets, 'replies': n_replies, 'hashtags': l_hashtags}

            self.collection.insert_one(post)


    def on_error(self, staus_code):
        # code to run each time an error is received
        if staus_code == 420:
            return False
        else:
            return True


def clean_text(text):
    clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
    clean_text = re.sub("(@.+)|(#.+)•", "", clean_text)
    clean_text = re.sub(r"https\S+", "", clean_text)
    clean_text = re.sub(r'[^\w]', ' ', clean_text)
    clean_text = clean_text.lower()
    return " ".join(clean_text.split())

def is_a_complain(text, freq_dict):
    value = 0
    repeated_words = []

    for i in range(len(freq_dict)):
        if freq_dict["WORD"][i] in text and freq_dict["WORD"][i] not in repeated_words:
            value += 1
            repeated_words.append(freq_dict["WORD"][i])

    return ((value / len(freq_dict)) >= 0.05)

def text_analysis(post, nlp, nlp_s, freq_dict,f):
    lemmatized = []
    stringed = ""
    text = clean_text(post['text'])
    obj = nlp(text)
    tokens = [tk.orth_ for tk in obj if not tk.is_punct | tk.is_stop]
    normalized = [tk.lower() for tk in tokens if len(tk) > 3 and tk.isalpha()]
    aux_json = ""

    for n in normalized:
        stringed = stringed + n + " "

    doc = nlp_s(stringed)

    for sent in doc.sentences:
        for word in sent.words:
            lemmatized.append(word.lemma)

    if(is_a_complain(lemmatized, freq_dict)):
        aux_json += "{\'link\':" + post['link'] + ", \'id\':" + post['id'] + ", \'text\':" + text + ", \'user\':" + post['user'] + ", \'date\':"\
                   + str(int(post['date'].timestamp())) +", \'likes\':" + str(post['likes']) + ", \'retweets\':" + str(post['retweets']) + ", \'replies\':" + str(post['replies']) + ", \'hashtags\':"
        aux_hashtags = "["
        for h in post['hashtags']:
            aux_hashtags+= (h['text'] + ", ")
        aux_hashtags += "]"

        aux_json += (aux_hashtags + "}, ")
        f.write(aux_json)




def main():

    freq_dict = pd.read_csv("../../dict/FREQUENCIES_DIC.csv")
    load_dotenv(find_dotenv("env/TwitterTokens.env"))
    tweepy_stream = SimpleListener(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'), os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'), daemon=True)
    tweepy_stream.filter(languages=['es'], threaded=True, track=[freq_dict["WORD"][0],freq_dict["WORD"][1],freq_dict["WORD"][2],freq_dict["WORD"][3],freq_dict["WORD"][4],freq_dict["WORD"][5],
                                                  freq_dict["WORD"][6],freq_dict["WORD"][7],freq_dict["WORD"][8],freq_dict["WORD"][9],freq_dict["WORD"][10],freq_dict["WORD"][11],
                                                  freq_dict["WORD"][12],freq_dict["WORD"][13],freq_dict["WORD"][14],freq_dict["WORD"][15],freq_dict["WORD"][16],freq_dict["WORD"][17],
                                                  freq_dict["WORD"][18],freq_dict["WORD"][19]])

    f = open("../../json/examples.json", 'a')
    f.write("[")
    client = MongoClient()
    db = client['tweet_stream']
    collection = db['test']

    nlp = spacy.load("es_core_news_sm")
    nlp_s = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')

    while(1):
        for post in collection.find():
            text_analysis(post, nlp, nlp_s, freq_dict,f)
            collection.delete_one({"_id": post['_id']})



if __name__ == "__main__":
    # calling main function
    main()