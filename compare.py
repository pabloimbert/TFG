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

# FOR THE MEDIAN
import statistics



def main():
    freq_dict = pd.read_csv("FREQUENCIES_DIC.csv")
    values_training = []
    values_random = []
    texts_training = []
    texts_random = []
    mdic_training = []
    mdic_random = []
    min_training = 100000
    min_random = 100000
    max_training = 0
    max_random = 0
    avg_training = 0
    avg_random = 0
    accumulative = 0


    with open("training.txt") as f:
        lines_training = f.read()

    with open("random_tweets.txt") as f:
        lines_random = f.read()

    texts_training = lines_training.split("#$%")
    texts_random = lines_random.split("\n")
    nlp = spacy.load("es_core_news_sm")
    nlp_s = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')

    for text in texts_training:
        value = 0
        dic = []
        lemmatized = []

        obj = nlp(text)
        tokens = [tk.orth_ for tk in obj if not tk.is_punct | tk.is_stop]
        normalized = [tk.lower() for tk in tokens if len(tk) > 3 and tk.isalpha()]

        for n in normalized:
            text = text + n + " "

        #stanza.download('es')
        doc = nlp_s(text)

        for sent in doc.sentences:
            for word in sent.words:
                lemmatized.append(word.lemma)

        for i in  range(len(freq_dict)):
            if freq_dict["WORD"][i] in lemmatized:
                value += len(freq_dict) - i
                dic.append(freq_dict["WORD"][i])

        accumulative += value

        if (value < min_training):
            min_training = value

        if (value > max_training):
            max_training = value

        values_training.append(value)
        mdic_training.append(dic)

    avg_training = accumulative/len(texts_training)
    accumulative = 0

    for text in texts_random:
        value = 0
        dic = []
        lemmatized = []

        obj = nlp(text)
        tokens = [tk.orth_ for tk in obj if not tk.is_punct | tk.is_stop]
        normalized = [tk.lower() for tk in tokens if len(tk) > 3 and tk.isalpha()]

        for n in normalized:
            text = text + n + " "

        #stanza.download('es')
        doc = nlp_s(text)

        for sent in doc.sentences:
            for word in sent.words:
                lemmatized.append(word.lemma)

        for i in  range(len(freq_dict)):
            if freq_dict["WORD"][i] in lemmatized:
                value += len(freq_dict) - i
                dic.append(freq_dict["WORD"][i])


        accumulative += value

        if (value < min_random):
            min_random = value

        if (value > max_random):
            max_random = value

        values_random.append(value)
        mdic_random.append(dic)
    avg_random = accumulative / len(texts_random)

    print("------------------------------     TRAINING.TXT     ------------------------------")
    print(values_training)
    print(mdic_training)
    print("MAX:", max_training, "MIN:", min_training, "AVG:", avg_training, "MEDIAN:", statistics.median(values_training))

    print("\n\n\n------------------------------     RANDOM_TWEETS.TXT     ------------------------------")
    print(values_random)
    print(mdic_random)
    print("MAX:", max_random, "MIN:", min_random, "AVG:", avg_random, "MEDIAN:", statistics.median(values_random))


if __name__ == "__main__":
    # calling main function
    main()

