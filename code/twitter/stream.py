import re
import tweepy
import emoji
import os
from dotenv import load_dotenv , find_dotenv
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

class SimpleListener(tweepy.StreamListener):
    def on_status(self, status):
        # code to run each time the stream receives a status

        # AQUI METERIAMOS EL STATUS EN MONGO
        print(status.text)

    def on_direct_message(self, status):
        # code to run each time the stream receives a direct message

        # AQUI METERIAMOS EL STATUS EN MONGO
        print(status.text)

    def on_data(self, status):
        # code to run each time you receive some data (direct message, delete, profile update, status,...)

        # AQUI METERIAMOS EL STATUS EN MONGO
        print(status.text)

    def on_error(self, staus_code):
        # code to run each time an error is received
        if staus_code == 420:
            return False
        else:
            return True



class TwitterClient(object):

    def __init__(self):
        # To set your environment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'

        # En este caso no tengo access_token y access_key sino bearer_token, pues al estar usando una cuenta para academic research solo tengo OAuth 2.0 en vez de OAuth 1.0

        load_dotenv(find_dotenv("env/TwitterTokens.env"))

        consumer_key = os.getenv('API_KEY')
        consumer_secret = os.getenv('API_KEY_SECRET')

        try:
            # creamos el objeto AppAuthHandler
            self.auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

            # Creamos el objeto de API de tweepy para acceder a los tweets
            self.api = tweepy.API(self.auth)

        except:
            print("ERROR: NO SE HA PODIDO AUTENTICAR")

def main():
    freq_dict = pd.read_csv("../dict/FREQUENCIES_DIC.csv")

    api = TwitterClient()
    tweepy_listener = SimpleListener()
    tweepy_stream = tweepy.Stream(auth=api.auth, listener=tweepy_listener())
    tweepy_stream.filter(languajes=['es'], track=[freq_dict["WORD"][0],freq_dict["WORD"][1],freq_dict["WORD"][2],freq_dict["WORD"][3],freq_dict["WORD"][4],freq_dict["WORD"][5],
                                                  freq_dict["WORD"][6],freq_dict["WORD"][7],freq_dict["WORD"][8],freq_dict["WORD"][9],freq_dict["WORD"][10],freq_dict["WORD"][11],
                                                  freq_dict["WORD"][12],freq_dict["WORD"][13],freq_dict["WORD"][14],freq_dict["WORD"][15],freq_dict["WORD"][16],freq_dict["WORD"][17],
                                                  freq_dict["WORD"][18],freq_dict["WORD"][19]])



if __name__ == "__main__":
    # calling main function
    main()