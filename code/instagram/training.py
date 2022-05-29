import re
import emoji
import pandas as pd
import keyring as kr
from instagrapi import Client
import statistics
# ----------------------------------------------------     FIXED VALUES     --------------------------------------------------------------

USERNAME = 'trabajosruineros'


class InstagramClient(object):

    # Method to initialize the Instagram Client. specify the username and it will get the credentials stored in the keyring
    def __init__(self):
        self.cl = Client()
        credential =kr.get_credential("system", "mentalrevolutionfdi")
        self.cl.login(credential.username,credential.password)

    # Method to clean the text for analyzing it. It strips it from emojis, symbols, links, hashtags and mentions, it also normalizes it.
    def clean_text(self, text):
        clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
        clean_text = re.sub("(@.+)|(#.+)•", "", clean_text)
        clean_text = re.sub(r"https\S+", "", clean_text)
        clean_text = re.sub(r'[^\w]', ' ', clean_text)
        clean_text = clean_text.lower()

        return " ".join(clean_text.split())

    def getMedia(self, userName):
        # Based on the username we get the user id
        user_id = self.cl.user_id_from_username(userName)
        # We get all posts from the user
        medias = self.cl.user_medias(user_id, 803)
        captions = []
        avg_array = []

        i = 0

        # We get the posts that were not used to create the dictionary, which are the 153 last posts
        for media in medias:
            if i > 650:
                # For each post we get its caption and clean it. We also save the length in words of each post
                media_caption = media.dict().get('caption_text')
                media_caption = self.clean_text(media_caption)
                text_len = len(media_caption.split())
                avg_array.append(text_len)
                captions.append(media_caption)

        column_names = ['Text', 'Prediction']
        data = []

        # Since we know that all these posts are indeed complaints we explicitly label them as complaints (giving them a prediction of 1)
        for caption in captions:
            data.append([caption, 1])

        # We keep these posts and their predictions in a csv called training.csv which will be used later.
        training = pd.DataFrame(data, columns=column_names)
        training.to_csv('../../text/training.csv')

        # We show the average and median length in words so we can later search for a corpus as similar as possible for the training.
        print("Average length ", statistics.mean(avg_array))
        print("Median length ", statistics.median(avg_array))



def main():
    # We initialize the Instagram Client and afterwards get the information regarding its posts from the fixed value USERNAME
    cli = InstagramClient()
    cli.getMedia(USERNAME)



if __name__ == "__main__":
    # calling main function
    main()