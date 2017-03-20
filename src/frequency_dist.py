#!/usr/bin/python

import os
from time import time
import sys

import unicodecsv as csv
from collections import defaultdict

import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

def progress_bar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces,
                                                    int(round(percent * 100))))
    sys.stdout.flush()

def get_text_word_freqs(df, frequencies):
    content = " ".join(df.text).decode("utf8")

    #words = content.split(" ") # vastly faster than ntlk.word_tokenize
    # punctuation = [".", "," ";", "!"]
    # words = [w for w in words if len(w) > 2 and "#" != w[0]]
    # words = [w for w in words if len(w) > 2 and "@" != w[0]]
    # words = [w[:-1] if len(w) >= 2 and w[-1] in punctuation else w for w in words]
    # for word in words:
    #     frequencies[word] += 1

    freqs = FreqDist(word_tokenize(content))
    for word, count in freqs.iteritems():
        frequencies[word] += count

    return frequencies

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
        df = pd.read_csv(os.path.join(DATA_PATH, file), low_memory=False)
        freqs = get_text_word_freqs(df, freqs)
        progress_bar(i, len(FILES), 50)
    msg = "\nTime to produce frequencies for all files: {:,.2f} minutes"
    print msg.format(len(FILES), (time() - start) / 60.0)

    print "Writing to outfile '{}'".format(OUTFILE)
    with open(OUTFILE, 'wb') as fout:
        dictionary_writer = csv.writer(fout)
        dictionary = zip(freqs.keys(), freqs.values())
        dictionary_writer.writerow(["word", "count"])
        for d in dictionary:
            dictionary_writer.writerow(d)

    print "Done."
