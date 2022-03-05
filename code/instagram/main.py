import stanza
from django.conf import settings
settings.configure()
from instagrapi import Client
from collections import Counter
import spacy
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


def main():
    cli = InstagramClient()
    cli.getMedia(USERNAME)



if __name__ == "__main__":
    # calling main function
    main()
