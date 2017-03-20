#!/usr/bin/python
from __future__ import division

import os
from time import time
import sys
import warnings

import unicodecsv as csv
from collections import defaultdict

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


type_errors=0

def progress_bar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write(
        "\rPercent: [{0}] {1}% | type errors: {2:,}".format(arrow + spaces,
                                                           int(round(percent * 100)),
                                                           type_errors))
    sys.stdout.flush()

def get_text_word_freqs(df, frequencies):
    global type_errors

    try:
        content = " ".join([str(s) for s in df.text]).decode("utf8")
    except:
        type_errors += 1
        raise ValueError(
            "Text value in a dataframe can't be coerced to string.")

    freqs = FreqDist(word_tokenize(content))
    for word, count in freqs.iteritems():
        frequencies[word] += count

    return frequencies

def compute_word_diversities(df, freqs):
    def word_diversity(t):
        """
        Get average word popularity for the given message
        """
        ws = word_tokenize(t)
        if len(ws) != 0:
            return sum([freqs[w] for w in ws]) / len(ws)
        else:
            return 0

    fs = df.text.apply(word_diversity)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError(
            "{} accepts 2 arguments, recieved {}".format(__file__,
                                                         len(sys.argv) - 1))

    DATA_PATH = os.path.abspath(sys.argv[1])
    OUTFILENAME = os.path.basename(sys.argv[2])
    TEST_LIMIT = int(sys.argv[3]) if len(sys.argv) >= 4 else None
    OUTFILE = os.path.join(os.path.dirname(DATA_PATH),
                           OUTFILENAME)
    FILES = os.listdir(DATA_PATH)
    if TEST_LIMIT:
        FILES = np.random.choice(FILES, TEST_LIMIT)

    print "Determining word counts for {} files in '{}':".format(len(FILES),
                                                                   DATA_PATH)
    start = time()
    freqs = defaultdict(int)
    for i, file in enumerate(FILES):
        progress_bar(i, len(FILES), 50)
        df = pd.read_csv(os.path.join(DATA_PATH, file))
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore",category=DeprecationWarning)
                freqs = get_text_word_freqs(df, freqs)
        except ValueError as ex:
            print ex.message
        progress_bar(i, len(FILES), 50)
    msg = "\nTime to produce frequencies for all files: {:,.2f} minutes"
    print msg.format(len(FILES), (time() - start) / 60.0)

    print "Writing to outfile '{}'".format(OUTFILE)
    with open(OUTFILE, 'wb') as fout:
        dictionary_writer = csv.writer(fout)
        dictionary = zip(freqs.keys(), freqs.values())
        dictionary_writer.writerow(["word", "count"])
        for d in dictionary:
            try:
                dictionary_writer.writerow(d)
            except Exception as ex:
                print "Error while writing '{}': {}".format(d, ex.message)

    print "Done."
