import re
import tweepy
import emoji
import os

from afinn import Afinn
from classifier import SentimentClassifier
from dotenv import load_dotenv, find_dotenv
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


class TwitterClient(object):

    def __init__(self):

        load_dotenv(find_dotenv("env/TwitterTokens.env"))
        consumer_key = os.getenv('API_KEY')
        consumer_secret = os.getenv('API_KEY_SECRET')

        try:
            # We create the object AppAuthHandler
            self.auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

            # Then create an API object so we can access all tweets from Twitter
            self.api = tweepy.API(self.auth)

        except:
            print("ERROR: UNABLE TO AUTHENTICATE")

    # Method to clean the text for analyzing it. It strips it from emojis, symbols, links, hashtags and mentions, it also normalizes it.
    def clean_text(self, text):

        clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
        clean_text = re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)", "", clean_text)
        clean_text = re.sub(r"https\S+", "", clean_text)
        return " ".join(clean_text.split())

    # This method gets all the images from a tweet if it has any.
    def get_images_from_tweet(self, tweet):
        images = set()

        if ('media' in tweet.entities):

            for image in tweet.extended_entities['media']:
                images.add(image['media_url'])

        return images

    # Method that retrieves tweets from an account given a username
    def get_all_tweets_from_user(self, screen_name):

        alltweets = []
        new_tweets = self.api.search_tweets(q='from:' + screen_name, count=200, lang="es")
        alltweets.extend(new_tweets)
        return alltweets

    # Method that calls get_all_tweets_from_user and for each tweet we keep those that are not empty and that have a negative sentiment analysis calculated with Afinn.
    def get_useful_tweets_Afinn(self, screen_name):

        afn = Afinn(language='es')
        tweets = self.get_all_tweets_from_user(screen_name)
        meaningful_tweets = []

        for tweet in tweets:
            text = self.clean_text(tweet.text)
            print(text + " " + str(afn.score(text)))
            if len(text) > 0 >= afn.score(text):
                meaningful_tweets.append(tweet)

        return meaningful_tweets

    # Method that calls get_all_tweets_from_user and for each tweet we keep those that are not empty and that have a negative sentiment analysis
    def get_useful_tweets(self, screen_name):

        tweets = self.get_all_tweets_from_user(screen_name)
        meaningful_tweets = []
        sentiment_classifier = SentimentClassifier()

        for tweet in tweets:
            if len(tweet.text) > 0 and sentiment_classifier.predict(tweet.text) <= 0.5:
                meaningful_tweets.append(tweet)

        return meaningful_tweets

    # Method that given a tweet retrieves all import information and gives it back in a JSON format.
    def retrieve_info_tweet(self, tweet):
        link = "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)
        tweet_id = tweet.id
        user = tweet.user.screen_name
        date = tweet.created_at
        n_likes = tweet.favorite_count
        n_retweets = tweet.retweet_count

        n_replies = 0
        replies = self.api.search_tweets(q='to:' + user, since_id=tweet_id)

        for reply in replies:
            if reply.in_reply_to_status_id == tweet_id:
                n_replies += 1

        # fetching the status
        status = self.api.get_status(tweet_id, tweet_mode="extended")
        text = self.clean_text(status.full_text)

        l_hashtags = []
        text_hashtags = text.split('#')

        i = 1
        for hashtag in text_hashtags:
            if i != 1:
                aux = hashtag.split(' ')
                l_hashtags.append(aux[0])
            i += 1

        dataset = pd.DataFrame(
            data={'link': [link], 'id': [tweet_id], 'text': [text], 'user': [user], 'date': [date], 'likes': [n_likes],
                  'retweets': [n_retweets], 'replies': [n_replies], 'hashtags': [l_hashtags]})
        dataset['date'] = dataset['date'].dt.strftime('%d/%m/%y - %H:%M')
        json_object = dataset.to_json(force_ascii=False, orient='records').replace('\/', '/')
        # json_object = json.dumps(dataset)
        # json_object = json.loads(json_object)
        return json_object


def main():
    api = TwitterClient()
    tweets = api.get_useful_tweets_Afinn(screen_name=SCREENNAME)
    json_array = []
    for tweet in tweets:
        json_array.append(api.retrieve_info_tweet(tweet))

    print('[')
    for json in json_array:
        print(json[1:-1])
    print(']')

    # os.chdir('text')
    f = open("../../json/examples.json", 'a')
    f.write('[')
    for json in json_array:
        f.write(json[1:-1])
        f.write("\n")
    f.write(']')


if __name__ == "__main__":
    # calling main function
    main()
