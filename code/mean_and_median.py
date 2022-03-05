import re
import emoji
import pandas as pd
import statistics


def clean_text(text):

    clean_text = re.sub(emoji.get_emoji_regexp(), " ", text)
    clean_text = re.sub("(@.+)|(#.+)•", "", clean_text)
    clean_text = re.sub(r"https\S+", "", clean_text)
    clean_text = re.sub(r'[^\w]', ' ', clean_text)
    clean_text = clean_text.lower()

    return " ".join(clean_text.split())

def getMedia():

    aux1 = pd.read_csv("../corpus/IMDB_Dataset_SPANISH.csv")
    aux2 = pd.read_csv("../corpus/punta_cana.csv")
    aux4 = pd.read_csv("../corpus/data_larazon_publico_v2.csv")
    text_IMDB = aux1['review_es']
    text_puntacana = aux2['review_text']
    text_larazon = aux4['cuerpo']
    avg_array = []
    i = 0

    for text in text_IMDB:
        if i == 152:
            break
        text = clean_text(text)
        text_len = len(text.split())
        avg_array.append(text_len)
        i+=1
    print("Average length IMDB ", statistics.mean(avg_array))
    print("Median length IMDB ", statistics.median(avg_array))

    avg_array = []
    i = 0

    for text in text_puntacana:
        if i == 152:
            break
        text = clean_text(text)
        text_len = len(text.split())
        avg_array.append(text_len)
        i += 1
    print("Average length puntacana ", statistics.mean(avg_array))
    print("Median length puntacana ", statistics.median(avg_array))


    avg_array = []
    i = 0

    for text in text_larazon:
        if i == 152:
            break
        text = clean_text(text)
        text_len = len(text.split())
        avg_array.append(text_len)
        i += 1
    print("Average length larazon ", statistics.mean(avg_array))
    print("Median length larazon ", statistics.median(avg_array))


def main():
    getMedia()


if __name__ == "__main__":
    # calling main function
    main()

