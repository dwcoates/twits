from __future__ import division

import os
from time import time
import sys
import warnings
import threading
from collections import defaultdict


import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from textblob import TextBlob

import itertools
import json
import ast

from twits.src import frequency_dist

def progress_bar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write(
        "\rPercent: [{0}] {1}% | type errors: {2:,}".format(arrow + spaces,
                                                           int(round(percent * 100)),
                                                           type_errors))
    sys.stdout.flush()

def get_text_word_freqs(df, words):
    return FreqDist(itertools.chain(*words))

def compute_word_diversities(df, freqs):
    def word_diversity(ws):
        """
        Get average word popularity for the given message
        """
        avg = np.mean([freqs[w] for w in ws])
        return avg if avg is not np.nan else 0

    return df.text.apply(word_diversity)

def compute_word_count(words):
    return words.apply(len)

def compute_text_sentiment(text):
    return text.apply(lambda t: TextBlob(t).sentiment.polarity).rename(
        "description_sentiment")

def compute_punctuation_usage(words):
    """
    Very stupid 'algorithm' for describing punctuation usage
    """
    def contains(v, p):
        for _p in p:
            if _p in v:
                return True
        return False

    good_punct = [",", ";", "'"]
    sorta_good_punct = [",", "."]
    sorta_bad_punct = ["!", "?"]

    v = 1

    if contains(words, good_punct):
        v *= 1.4
    if contains(words, sorta_good_punct):
        v *= 1.1
    if contains(words, sorta_bad_punct):
        v *= 0.85

    return v

def get_hashtags(hashtags):
    return hashtags.apply(ast.literal_eval)

def get_user_mentions(user_mentions):
    return user_mentions.apply(ast.literal_eval)

def compute_hashtag_info(tags, freqs):
    return tags.apply(lambda tgs: np.mean([freqs[t] for t in tgs])).fillna(0)

def compute_user_mention_info(tags, freqs):
    return tags.apply(lambda tgs: np.mean([freqs[t] for t in tgs])).fillna(0)

def get_hashtag_freqs(hashtags):
    tags = itertools.chain(*hashtags)
    d = defaultdict(int)
    for t in tags:
        d[t] += 1

    return d

def get_user_mention_freqs(user_mentions):
    tags = itertools.chain(*user_mentions)
    d = defaultdict(int)
    for t in tags:
        d[t] += 1

    return d

def compute_user_mention_freq(user_mentions, freq):
    return user_mentions.apply(lambda x: np.mean([freq[m] for m in x]))

def compute_hashtag_freq(hashtags, freq):
    return hashtags.apply(lambda x: np.mean([freq[m] for m in x]))

def process_text_attributes(df):
    start = time()
    sys.stdout.write("Tokenizing text words...\r")
    threads = []
    num_threads = 8
    words = [None] * num_threads
    texts = np.array_split(df.text, num_threads)
    for i in range(num_threads):
        def process_tokens():
            words[i] = texts[i].apply(word_tokenize)
        t = threading.Thread(target=process_tokens)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    words = pd.concat(words)
    # single-threaded version:
    ### words = df.text.apply(word_tokenize)
    print "Time to tokenize: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Tallying word frequencies...\r")
    freqs = get_text_word_freqs(df, words)
    print "Time to text tally frequencies: {:,.2f} seconds".format(
        (time() - start))

    start = time()
    sys.stdout.write("Computing text sentiment polarity...\r")
    df["sentiment"] = compute_text_sentiment(df.text)
    print "Time to determine text sentiment: {:,.2f} seconds".format(
        (time() - start))

    start = time()
    sys.stdout.write("Computing text word diversity...\r")
    df["text_diversity"] = compute_word_diversities(df, freqs)
    df["word_count"] = compute_word_count(words)
    print "Time to compute text word diversity: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Parsing hashtags and user_mentions...\r")
    hashtags = get_hashtags(df.entities_hashtags)
    user_mentions = get_user_mentions(df.entities_hashtags)
    print "Time to parse hashtags and mentions: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Tallying hashtags and user_mentions freqencies...\r")
    hashtag_freqs = get_hashtag_freqs(hashtags)
    user_mention_freqs = get_user_mention_freqs(user_mentions)
    print "Time to tally hashtag and mention frequencies: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write(
        "Computing hashtag and user_mentions diversity...\r")
    df["hashtag_count"] = hashtags.apply(len)
    df["user_mentions_count"] = user_mentions.apply(len)
    df["user_hashtag_freq"] = compute_hashtag_info(hashtags, hashtag_freqs)
    df["user_mention_freq"] = compute_user_mention_info(user_mentions,
                                                        user_mention_freqs)
    print "Time to computer hashtag and mention diversity: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Tokenizing retweet text words...\r")
    threads = []
    num_threads = 8
    words = [None] * num_threads
    texts = np.array_split(df.retweet_text, num_threads)
    for i in range(num_threads):
        t = threading.Thread(target=process_tokens)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    words = pd.concat(words)
    # single-threaded version:
    ### words = df.text.apply(word_tokenize)
    print "Time to tokenize retweet text: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Tallying retweet text word frequencies...\r")
    freqs = get_text_word_freqs(df, words)
    print "Time to text tally frequencies: {:,.2f} seconds".format(
        (time() - start))

    start = time()
    sys.stdout.write("Computing retweet text sentiment polarity...\r")
    df["retweet_sentiment"] = compute_text_sentiment(df.retweet_text)
    print "Time to determine text sentiment: {:,.2f} seconds".format(
        (time() - start))

    start = time()
    sys.stdout.write("Computing retweet text word diversity...\r")
    df["retweet_text_diversity"] = compute_word_diversities(df, freqs)
    df["retweet_word_count"] = compute_word_count(words)
    print "Time to compute text word diversity: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Parsing retweet hashtags and user_mentions...\r")
    hashtags = get_hashtags(df.retweet_hashtags)
    user_mentions = get_user_mentions(df.retweet_user_mentions)
    print "Time to parse hashtags and mentions: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Tallying retweet hashtags and user_mentions freqencies...\r")
    hashtag_freqs = get_hashtag_freqs(hashtags)
    user_mention_freqs = get_user_mention_freqs(user_mentions)
    print "Time to tally hashtag and mention frequencies: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write("Computing retweet punctuation usage...\r")
    df["retweet_punctuation_score"] = compute_punctuation_usage(words)
    print "Time to compute punctuation usage: {:,.2f} seconds".format(
        time() - start)

    start = time()
    sys.stdout.write(
        "Computing hashtag and user_mentions diversity...\r")
    df["retweet_hashtag_count"] = hashtags.apply(len)
    df["retweet_user_mentions_count"] = user_mentions.apply(len)
    df["retweet_hashtag_freq"] = compute_hashtag_info(hashtags, hashtag_freqs)
    df["retweet_user_mention_freq"] = compute_user_mention_info(user_mentions,
                                                        user_mention_freqs)
    print "Time to computer hashtag and mention diversity: {:,.2f} seconds".format(
        time() - start)



    return df.drop(["entities_hashtags", "entities_user_mentions", "retweet_hashtags", "retweet_user_mentions"], axis=1)
