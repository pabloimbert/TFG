import re

from classifier import SentimentClassifier
from django.conf import settings
settings.configure()

# TO COLLECT THE TWEETS
import tweepy
import os
from dotenv import load_dotenv , find_dotenv

# TO FILTER THE EMOJIS FROM THE TEXT
import emoji
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class TwitterClient(object):

    def __init__(self):

        load_dotenv(find_dotenv("../../env/TwitterTokens.env"))

        consumer_key = os.getenv('API_KEY')
        consumer_secret = os.getenv('API_KEY_SECRET')

        try:
            # We create the object AppAuthHandler
            self.auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

            # Then create an API object so we can access all tweets from Twitter
            self.api = tweepy.API(self.auth)

        except:
            print("ERROR: UNABLE TO AUTHENTICATE")

    def get_all_tweets_from_query(self):
            alltweets = []
            # We get all tweets that do not have any media, that are not retweets, quoted tweets or replies and that are in spanish
            new_tweets = self.api.search_tweets(q="-filter:media -filter:retweets -filter:quote -filter:replies", lang="es")

            # guardamos estos tweets en nuestro array de todos los tweets
            alltweets.extend(new_tweets)

            return alltweets

    # Method to clean the text for analyzing it. It strips it from emojis, symbols, links, hashtags and mentions, it also normalizes it.
    def clean_text(self, text):

        clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
        clean_text = re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)", "", clean_text)
        clean_text = re.sub(r"https\S+", "", clean_text)

        return " ".join(clean_text.split())

    # Method that calls get_all_tweets_from_query and for each tweet we keep those that are not empty and that have a negative sentiment analysis.
    def get_useful_tweets(self):
        tweets = self.get_all_tweets_from_query()
        meaningful_tweets = []
        sentiment_classifier = SentimentClassifier()

        for tweet in tweets:
            if len(tweet.text) > 0 and sentiment_classifier.predict(tweet.text) <= 0.5:
                status = self.api.get_status(tweet.id, tweet_mode="extended")
                text = self.clean_text(status.full_text)
                link = "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)
                print(link)
                meaningful_tweets.append(text)

        return meaningful_tweets

# We create the twitter Client to connect with the api and save random tweets so we can later test the algorithm built for instagram
# with tweets instead of posts
def main():
    api = TwitterClient()
    tweets = api.get_useful_tweets()
    os.chdir('text')
    f = open("random_tweets.txt", 'a')

    for tweet in tweets:
        f.write(tweet.replace("\n", " "))
        f.write("\n")



if __name__ == "__main__":
    # calling main function
    main()
