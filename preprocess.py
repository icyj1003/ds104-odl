import emoji
import numpy as np
import re
import py_vncorenlp

py_vncorenlp.download_model(save_dir='C:/Users/ADMIN/Desktop/odl/vncorenlp')

rdrsegmenter = py_vncorenlp.VnCoreNLP(
    annotators=["wseg"], save_dir='C:/Users/ADMIN/Desktop/odl/vncorenlp')

STOPWORDS = 'C:/Users/ADMIN/Desktop/odl/resources/vietnamese-stopwords.txt'
with open(STOPWORDS, "r", encoding='utf8') as ins:
    stopwords = []
    for line in ins:
        dd = line.strip('\n')
        stopwords.append(dd)
    stopwords = set(stopwords)


def filter_stop_words(train_sentences, stop_words):
    new_sent = [word for word in train_sentences.split()
                if word not in stop_words]
    train_sentences = ' '.join(new_sent)

    return train_sentences


def deEmojify(text):
    text = re.sub(r'http\S+', '', text)
    return emoji.replace_emoji(text)


def clean(text, tokenized=True, lowercased=True, removestopword=True):
    text = filter_stop_words(text, stopwords) if removestopword else text
    text = deEmojify(text)
    
    text = text.lower() if lowercased else text

    if tokenized:
        pre_text = ""
        sentences = rdrsegmenter.word_segment(text)
        for sentence in sentences:
            pre_text += "".join(sentence)
        text = pre_text

    return text.split()
