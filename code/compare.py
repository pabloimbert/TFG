import re
import stanza

from django.conf import settings
settings.configure()
import pandas as pd
import spacy
import emoji
from sklearn import metrics

def clean_text(text):

    clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
    clean_text = re.sub("(@.+)|(#.+)•", "", clean_text)
    clean_text = re.sub(r"https\S+", "", clean_text)
    clean_text = re.sub(r'[^\w]', ' ', clean_text)
    clean_text = clean_text.lower()

    return " ".join(clean_text.split())

def main():

    #os.chdir('dict')
    freq_dict = pd.read_csv("../dict/FREQUENCIES_DIC.csv")
    labels = []
    processed_labels = []

    news_2 = pd.read_csv("../corpus/IMDB_Dataset_SPANISH.csv")
    texts_news = news_2['review_es']

    words_in_dic = []
    texts = []


    #WE KNOW THAT NONE OF THESE ARTICLES ARE COMPLAINTS
    for news in texts_news:
        labels.append(0)
        texts.append(news)

    training = pd.read_csv("../text/training.csv")
    texts_training = training['Text']

    for text in texts_training:
        labels.append(1)
        texts.append(text)

    nlp = spacy.load("es_core_news_sm")
    nlp_s = stanza.Pipeline(lang='es', processors='tokenize,mwt,pos,lemma')


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
        aux = []
        repeated_words = []
        for i in range(len(freq_dict)):
            if freq_dict["WORD"][i] in lemmatized and freq_dict["WORD"][i] not in repeated_words:
                value+=1
                repeated_words.append(freq_dict["WORD"][i])
                aux.append(freq_dict["WORD"][i])

        words_in_dic.append(aux)

        if (value/len(freq_dict) >= 0.0533):
            processed_labels.append(1)
        else:
            processed_labels.append(0)
#############################################################


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
        aux = []

        for i in range(len(freq_dict)):
            if freq_dict["WORD"][i] in lemmatized and freq_dict["WORD"][i] not in repeated_words:
                value += 1
                repeated_words.append(freq_dict["WORD"][i])
                aux.append(freq_dict["WORD"][i])
        words_in_dic.append(aux)

        if (value/len(freq_dict) >= 0.0533):
            processed_labels.append(1)
        else:
            processed_labels.append(0)







    print("----------------------- TRUE POSITIVES -----------------------")
    for i in range(len(labels)):
        if processed_labels[i] == labels[i] and labels[i] == 1:
            print(texts[i], "\n")
            print(words_in_dic[i], "\n")

    print("\n\n----------------------- TRUE NEGATIVES -----------------------")
    for i in range(len(labels)):
        if processed_labels[i] == labels[i] and labels[i] == 0:
            print(texts[i], "\n")
            print(words_in_dic[i], "\n")

    print("\n\n----------------------- FALSE POSITIVES -----------------------")
    for i in range(len(labels)):
        if processed_labels[i] != labels[i] and labels[i] == 0:
            print(texts[i], "\n")
            print(words_in_dic[i], "\n")

    print("\n\n----------------------- FALSE NEGATIVES -----------------------")
    for i in range(len(labels)):
        if processed_labels[i] != labels[i] and labels[i] == 1:
            print(texts[i], "\n")
            print(words_in_dic[i], "\n")




    cm_results = metrics.confusion_matrix(labels, processed_labels)
    print(cm_results)
    print(f'Accuracy: {round(metrics.accuracy_score(labels, processed_labels), 2)}')
    print(f'Recall: {round(metrics.recall_score(labels, processed_labels), 2)}')
    print(f'ROC-AUC: {round(metrics.roc_auc_score(labels, processed_labels), 2)}')
    print(f'Precision: {round(metrics.precision_score(labels, processed_labels), 2)}')
    print(f'F1: {round(metrics.f1_score(labels, processed_labels), 2)}')

    #for label in processed_labels:



if __name__ == "__main__":
    # calling main function
    main()