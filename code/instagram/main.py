import stanza
from django.conf import settings
settings.configure()
from instagrapi import Client
from collections import Counter
import spacy
# ----------------------------------------------------     FIXED VALUES     --------------------------------------------------------------

USERNAME = 'trabajosruineros'

class InstagramClient(object):

    # Method to initialize the Instagram Client. To login in the first argument has to be a username and the second the password of that user
    def __init__(self):
        self.cl = Client()
        self.cl.login('XXXXX', 'XXXXX')


    def getMedia(self, userName):
        # Based on the username we get the user id
        user_id = self.cl.user_id_from_username(userName)
        # We get the first 650 posts from the user
        medias = self.cl.user_medias(user_id, 650)
        captions = []
        lemmatized = []
        every_word = ""
        text = ""
        # We previously studied the account, and so determined which posts were ads instead of real posts, and decided to take them out
        # so it does not bias the result.
        irrelevant_posts = [31, 213, 386, 499, 631]
        i = 0

        # We keep all posts text in the same string, so we can analyze it more easily.
        for media in medias:
            if i not in irrelevant_posts:
                media_caption = media.dict().get('caption_text')
                captions.append(media_caption)
                every_word = every_word + " " + media_caption
            i = i + 1

        # We tokenize and normalize the string specifying that it is an spanish text
        nlp = spacy.load("es_core_news_sm")
        obj = nlp(every_word)
        tokens = [tk.orth_ for tk in obj if not tk.is_punct | tk.is_stop]
        normalized = [tk.lower() for tk in tokens if len(tk) > 3 and tk.isalpha()]

        # We add together the whole normalized array into a string again.
        for n in normalized:
            text = text + n + " "

        # stanza does only need to be download the first time it is executed, later it can be commented out
        stanza.download('es')
        nlp = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')
        doc = nlp(text)

        # For each word we keep its lemma
        for sent in doc.sentences:
            for word in sent.words:
                lemmatized.append(word.lemma)

        # Finally, we order the lemmas by its frequency
        freq = Counter(lemmatized).most_common()
        print(freq)


def main():
    # We initialize the Instagram Client and afterwards get the information regarding its posts from the fixed value USERNAME
    cli = InstagramClient()
    cli.getMedia(USERNAME)



if __name__ == "__main__":
    # calling main function
    main()
