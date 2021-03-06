from __future__ import print_function
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

import sys
import os
import re
# http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf_lda.html


n_samples = 2000
n_features = 1000
n_topics = 10
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join(
            [feature_names[i]
                for i in topic.argsort()[:-n_top_words - 1:-1]]
            )
        )
    print()


def run_nmf(directory):
    print("Loading dataset...")
    t0 = time()

    data_samples = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath) as f:
            lyrics = f.read()
            f.close()
        pattern = re.compile('\[(.*?)\]')
        cleaned_lyrics = pattern.sub('', lyrics)
        data_samples.append(cleaned_lyrics)
    print("done in %0.3fs." % (time() - t0))

    print("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.95,
        min_df=2,
        max_features=n_features,
        stop_words='english'
    )
    t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(data_samples)
    print("done in %0.3fs." % (time() - t0))

    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(
        max_df=0.95,
        min_df=2,
        max_features=n_features,
        stop_words='english'
    )
    t0 = time()
    tf = tf_vectorizer.fit_transform(data_samples)
    print("Done in %0.3fs." % (time() - t0))

    t0 = time()
    tf = tf_vectorizer.fit_transform(data_samples)
    print("done in %0.3fs." % (time() - t0))

    print("Fitting the NMF model with tf-idf features, "
        "n_samples=%d and n_feautres=%d..."
        % (n_samples, n_features))

    t0 = time()
    nmf = NMF(
        n_components=n_topics,
        random_state=1,
        alpha=.1,
        l1_ratio=.5
        ).fit(tfidf)
    print("done in %0.3fs." % (time() - t0))

    print("\nTopics in NMP model:")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, n_top_words)

    print("fitting LDA models with tf features, "
        "n_samples=%d and n_features=%d..."
        % (n_samples, n_features))
    lda = LatentDirichletAllocation(
        n_topics=n_topics,
        max_iter=5,
        learning_method='online',
        learning_offset=50.,
        random_state=0
    )

    t0 = time()
    lda.fit(tf)
    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)
