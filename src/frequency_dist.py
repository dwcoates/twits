import os
from time import time
import sys

import unicodecsv as csv
from collections import defaultdict

import pandas as pd

def get_text_word_freqs(df, frequencies=defaultdict(int)):
    start = time()

    sys.stdout.flush()
    sys.stdout.write("Building corpus...\r")
    content = " ".join(df.text).decode("utf8")

    sys.stdout.flush()
    sys.stdout.write("Tokenizing words...\r")
    words = content.split(" ") # vastly faster than ntlk.word_tokenize

    sys.stdout.flush()
    sys.stdout.write("Dropping hashtags...\r")
    words = [w for w in words if len(w) > 2 and "#" in w]

    sys.stdout.flush()
    sys.stdout.write("Accumulating frequencies...\r")
    for word in words:
        frequencies[word] += 1

    msg = "Time to produce frequencies for corpus of {:,} words: {:.2f} seconds"
    print msg.format(len(words), time() - start)

    return frequencies

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError(
            "{} accepts 2 arguments, recieved {}".format(
                __file__,
                len(sys.argv) - 1))

    DATA_PATH = os.path.abspath(sys.argv[1])
    OUTFILENAME = os.path.abspath(sys.argv[2])
    OUTFILE = os.join(os.path.abspath(DATA_PATH),
                      os.path.(OUTFILENAME))
    FILES = os.listdir(DATA_PATH)

    print "Determining word counts for {} files in '{}':\n".format(len(FILES),
                                                                   DATA_PATH)
    freqs = defaultdict(int)
    for file in FILES:
        freqs = get_text_word_freqs(file)

    print "Writing to outfile '{}'".format(OUTFILE)
    dictionary_writer = csv.writer(OUTFILE)
    dictionary = zip(*freqs.keys(), *freqs.values())
    dictionary_writer.writerow(["word", "count"])
    for d in dictionary:
        dictionary_writer.writerow(d)

    print "Done."
