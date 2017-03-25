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
    tags = df.entities_hashtags.apply(ast.literal_eval)
    return tags.apply(lambda tg: [t["text"] for t in tg])

def get_user_mentions(df):
    mentions = df.entities_user_mentions.apply(ast.literal_eval)
    return mentions.apply(lambda tg: [t["screen_name"] for t in tg])

def compute_hashtag_info(tags, freqs):
    return tags.apply(lambda tgs: np.mean([freqs[t] for t in tgs]))

def compute_user_mention_info(tags, freqs):
    return tags.apply(lambda tgs: np.mean([freqs[t] for t in tgs]))

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
    df["user_hashtag_freq"] = compute_hashtag_info(hashtags, hashtag_freqs)
    df["user_mention_freq"] = compute_user_mention_info(user_mentions,
                                                        user_mention_freqs)

    return df.drop(["entities_hashtags", "entities_user_mentions"], axis=1)
