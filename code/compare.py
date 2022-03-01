# Cargar en formato dataframe el diccionario
# Cargar textos de prueba
# Comparar porcentajes del diccionario en los textos
import re
import numpy as np
import stanza

from django.conf import settings
settings.configure()
import pandas as pd
import spacy
import emoji
from sklearn import metrics
# FOR THE MEDIAN
import statistics


def clean_text(self, text):
    clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
    clean_text = re.sub("(@.+)|(#.+)•", "", clean_text)
    clean_text = re.sub(r"https\S+", "", clean_text)
    clean_text = re.sub(r'[^\w]', ' ', clean_text)
    clean_text.toLowerCase()

    return " ".join(clean_text.split())

def main():
    freq_dict = pd.read_csv("../dict/FREQUENCIES_DIC.csv")
    texts_training = []
    texts_news = []
    min_training = 100000
    min_news = 100000
    max_training = 0
    max_news = 0
    accumulative = 0
    texts_news = []
    labels = []
    processed_labels = []

    news_2 = pd.read_csv("../text/development.csv")

    texts_news.append(news_2['Text'])

    #WE KNOW THAT NONE OF THESE ARTICLES ARE COMPLAINTS
    for news in news_2:
            labels.append(0)

    training = pd.read_csv("../text/training.txt")
    texts_training.append(training['Text'])

    for text in texts_training:
        labels.append(1)

    nlp = spacy.load("es_core_news_sm")
    nlp_s = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')

    accumulative = 0

    for text in texts_news:
        value = 0
        lemmatized = []
        stringed = ""

        text = clean_text(text)
        obj = nlp(text)
        tokens = [tk.orth_ for tk in obj if not tk.is_punct | tk.is_stop]
        normalized = [tk.lower() for tk in tokens if len(tk) > 3 and tk.isalpha()]

        for n in normalized:
            stringed = stringed + n + " "

        # stanza.download('es')
        doc = nlp_s(stringed)

        for sent in doc.sentences:
            for word in sent.words:
                lemmatized.append(word.lemma)
#############################################################
        repeated_words = []
        for i in range(len(freq_dict)):
            if freq_dict["WORD"][i] in lemmatized and freq_dict["WORD"][i] not in repeated_words:
                value+=1
                repeated_words.append(freq_dict["WORD"][i])
        processed_labels.append(value / len(freq_dict))
#############################################################
        accumulative += value
        if (value < min_news):
            min_news = value

        if (value > max_news):
            max_news = value


    avg_news = accumulative / len(texts_news)

    for text in texts_training:
        value = 0
        lemmatized = []
        stringed = ""

        text = clean_text(text)
        obj = nlp(text)
        tokens = [tk.orth_ for tk in obj if not tk.is_punct | tk.is_stop]
        normalized = [tk.lower() for tk in tokens if len(tk) > 3 and tk.isalpha()]

        for n in normalized:
            stringed = stringed + n + " "

        #stanza.download('es')
        doc = nlp_s(stringed)

        for sent in doc.sentences:
            for word in sent.words:
                lemmatized.append(word.lemma)

        repeated_words = []
        for i in range(len(freq_dict)):
            if freq_dict["WORD"][i] in lemmatized and freq_dict["WORD"][i] not in repeated_words:
                value += 1
                repeated_words.append(freq_dict["WORD"][i])
        processed_labels.append(value / len(freq_dict))
        accumulative += value

        if (value < min_training):
            min_training = value

        if (value > max_training):
            max_training = value



    avg_training = accumulative/len(texts_training)

    cm_results = metrics.confusion_matrix(labels, processed_labels)
    print(cm_results)
    print(f'Accuracy: {round(metrics.accuracy_score(labels, processed_labels), 2)}')
    print(f'Recall: {round(metrics.recall_score(labels, processed_labels), 2)}')
    print(f'ROC-AUC: {round(metrics.roc_auc_score(labels, processed_labels), 2)}')
    print(f'Precision: {round(metrics.precision_score(labels, processed_labels), 2)}')
    print(f'F1: {round(metrics.f1_score(labels, processed_labels), 2)}')

    #print("------------------------------     TRAINING.TXT     ------------------------------")
    #print(labels)
    #print("MAX:", max_training, "MIN:", min_training, "AVG:", avg_training, "MEDIAN:", statistics.median(values_training))

    #print("\n\n\n------------------------------     RANDOM_TWEETS.TXT     ------------------------------")
    #print(processed_labels)
    #print("MAX:", max_news, "MIN:", min_news, "AVG:", avg_news, "MEDIAN:", statistics.median(values_random))


if __name__ == "__main__":
    # calling main function
    main()

