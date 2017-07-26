import re
import sys
import os

from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models


def playlist_lda(directory, num_topics=2, num_words=10):
    tokenized_text = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        tokens = preprocess_text(filepath)
        tokenized_text.append(tokens)

    get_lda_topics(tokenized_text, num_topics, num_words)


def preprocess_text(filepath):
    lyrics = read_lyrics(filepath)
    tokens = tokenize_by_word(lyrics)
    tokenized_text = clean_stop_words(tokens)
    return tokenized_text


def get_lda_topics(array_of_lyrics, num_topics, num_words):
    dictionary = corpora.Dictionary(array_of_lyrics)
    corpus = [dictionary.doc2bow(text) for text in array_of_lyrics]
    ldamodel = models.ldamodel.LdaModel(
        corpus,
        num_topics,
        id2word=dictionary,
        passes=20)
    print(ldamodel.print_topics(num_topics, num_words))


def tokenize_by_word(lyrics):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = []
    for line in lyrics:
        raw = line.lower().decode('utf-8')
        raw_tokens = tokenizer.tokenize(raw)
        tokens = tokens + raw_tokens
    return tokens


def clean_stop_words(tokenized_lyrics):
    en_stop = get_stop_words('en')
    en_stop.append('yeah')
    stopped_tokens = [
        token for token
        in tokenized_lyrics
        if token not in en_stop and len(token) > 1]
    # remove single letters, does not take
    # care of contractions (e.g. I'm very well)
    return stopped_tokens


def read_lyrics(filename):
    with open(filename) as f:
        lyrics = f.readlines()
        f.close()

    pattern = re.compile('\[(.*?)\]')

    strip_verse_markers = [pattern.sub('', line.strip()) for line in lyrics]
    content = [line for line in strip_verse_markers if line != '']
    return content
