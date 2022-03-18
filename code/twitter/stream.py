import re
import tweepy
import emoji
import os
from dotenv import load_dotenv , find_dotenv
from pymongo import MongoClient
import pandas as pd
import ssl


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
        # code to run each time the stream receives a status
        l_hashtags=[]
        tweet_id = status.id_str

        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                text = status.retweeted_status.extended_tweet['full_text']
                l_hashtags = status.retweeted_status.extended_tweet['entities']['hashtags']
            except AttributeError:
                text = status.retweeted_status.text
                l_hashtags = status.retweeted_status.entities['hashtags']
        else:
            try:
                text = status.extended_tweet["full_text"]
                l_hashtags = status.extended_tweet['entities']['hashtags']
            except AttributeError:
                text = status.text
                l_hashtags = status.entities['hashtags']


        user = status.user.screen_name
        link = "https://twitter.com/" + user + "/status/" + tweet_id

        date = status.created_at
        n_likes = status.favorite_count
        n_retweets = status.retweet_count
        n_replies = status.reply_count


        post = {'link': link, 'id': tweet_id, 'text': text, 'user': user, 'date': date, 'likes': n_likes,
         'retweets': n_retweets, 'replies': n_replies, 'hashtags': l_hashtags}

        self.collection.insert_one(post)
        print("on_status")

    def on_error(self, staus_code):
        # code to run each time an error is received
        if staus_code == 420:
            return False
        else:
            return True

def main():

    freq_dict = pd.read_csv("../../dict/FREQUENCIES_DIC.csv")
    load_dotenv(find_dotenv("env/TwitterTokens.env"))
    tweepy_stream = SimpleListener(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'), os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'),daemon = True)
    tweepy_stream.filter(languages=['es'], track=[freq_dict["WORD"][0],freq_dict["WORD"][1],freq_dict["WORD"][2],freq_dict["WORD"][3],freq_dict["WORD"][4],freq_dict["WORD"][5],
                                                  freq_dict["WORD"][6],freq_dict["WORD"][7],freq_dict["WORD"][8],freq_dict["WORD"][9],freq_dict["WORD"][10],freq_dict["WORD"][11],
                                                  freq_dict["WORD"][12],freq_dict["WORD"][13],freq_dict["WORD"][14],freq_dict["WORD"][15],freq_dict["WORD"][16],freq_dict["WORD"][17],
                                                  freq_dict["WORD"][18],freq_dict["WORD"][19]])


if __name__ == "__main__":
    # calling main function
    main()