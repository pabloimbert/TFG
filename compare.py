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

def main():
    freq_dict = pd.read_csv("FREQUENCIES_DIC.csv")
    values = []
    texts = []
    mdic = []
    with open("training.txt") as f:
        lines = f.read()

    texts = lines.split("#$%")
    nlp = spacy.load("es_core_news_sm")
    nlp_s = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')

    for text in texts:
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


        values.append(value)
        mdic.append(dic)
    print(values);
    print(mdic)


if __name__ == "__main__":
    # calling main function
    main()

