from __future__ import division

import os
from time import time
import sys
import warnings

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from collections import defaultdict

import itertools
import json
import ast

from src import frequency_dist

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
        if len(ws) != 0:
            return sum([freqs[w] for w in ws]) / len(ws)
        else:
            return 0

    return df.text.apply(word_diversity)

def compute_word_count(words):
    return words.apply(len)

def get_hashtags(df):
    return df.entities_hashtags.apply(ast.literal_eval)

def get_user_mentions(df):
    return df.entities_user_mentions.apply(ast.literal_eval)

def compute_hashtag_info(tags, freqs):
    return [freqs[t] for t in tags] / len(tags)

def compute_user_mention_info(tags, freqs):
    return [freqs[t] for t in tags] / len(tags)

def get_hashtag_freqs(hashtags):
    tags = itertools.chain(*hashtags)
    d = defaultdict(int)
    for t in tags:
        d[t] += 1

    return sum(d.values())/len(d.keys())

def get_user_mention_freqs(user_mentions):
    tags = itertools.chain(*user_mentions)
    d = defaultdict(int)
    for t in tags:
        d[t] += 1

    return d

def compute_user_mention_freq(user_mentions, freq):
    return user_mentions.apply(lambda x: sum([freq[m] for m in x])/len(x))

def compute_hashtag_freq(hashtags, freq):
    return hashtags.apply(lambda x: sum([freq[m] for m in x])/len(x))

def process_text_attribute(df):
    words = df.text.apply(word_tokenize)
    freqs = get_text_word_freqs(df, words)
    df["text_diversity"] = compute_word_diversities(df, freqs)
    df["word_count"] = compute_word_count(words)

    hashtags = get_hashtags(df)
    user_mentions = get_user_mentions(df)
    hashtag_freqs = get_hashtag_freqs(hashtags)
    user_mention_freqs = get_user_mention_freqs(user_mentions)

    df["hashtag_count"] = hashtags.apply(len)
    df["user_mentions_count"] = user_mentions.apply(len)

    hash_freqs = get_hashtag_freqs(df.entities_hashtags)
    user_mention_freqs = get_user_mention_freqs(df.user_mentions)
    df["user_hashtag_freq"] = compute_hashtag_freq(df.entities_user_mentions, freqs)
    df["user_mention_freq"] = compute_hashtag_freq(df.entities_user_mentions, freqs)
