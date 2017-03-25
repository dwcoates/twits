from __future__ import division

import os
from time import time
import sys
import warnings

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

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

def get_hashtags(entities_hashtags):
    return entities_hashtags.apply(ast.literal_eval)

def process_text_attribute(df):
    words = df.text.apply(word_tokenize)
    freqs = get_text_word_freqs(df, words)
    df["text_diversity"] = compute_word_diversities(df, freqs)
    df["word_count"] = compute_word_count(words)
    df["hashtag_count"] = compute_hashtag_count()
