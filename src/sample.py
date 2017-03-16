#!/usr/bin/python

import os
import time
import csv
import sys
import logging

import pandas as pd

from twits.src import preprocessing


logging.basicConfig(filename="../data/sample.log", level=logging.DEBUG)


def sample_rows(filename, portion):
    """
    Sample a some number of rows of ``filename`` according to ``portion``,
    which is a number between 0 and 1 indicating the percentage of rows to
    randomly sample *without* replacement.
    """

    start = time.time()
    df = pd.read_csv("../data/csv/data_sample.csv")
    read_time = time.time() - start

    num_samples = int(len(df.index) * portion)

    return pd.DataFrame.sample(n = num_samples).to_records()

def sample_files(directory, output_filename, portion):
    """
    Return a dataframe constructed from a portion of all csv files in
    directory.
    """

    FILES = os.listdir(os.path.abspath(directory))
    FILENAME = os.path.join(directory, output_filename)

    with open(FILENAME, 'wb') as fout:
        sample_writer = csv.writer(fout)
        sample_writer.writerow(preprocess.HEADERS)
        for i, f in enumerate(FILES):
            print "\n[{}/{}]".format(i+1, len(FILES))
            if "csv" != f.split(".")[-1]:
                print "Skipping '{}' for sampling.".format(f)
                continue
            try:
                rows = sample_rows(f, portion)
                for i, row in enumerate(rows):
                    if len(row)-1 == len(HEADERS):
                        sample_writer.writerow(row)
                    else:
                        msg = "Row #{} from '{}' has {} elements. It should have {}"
                        raise ValueError(msg.format(i+1, f, len(row)-1, len(HEADERS)))
            except ValueError as ex:
                logging.warn("WARNING: {}".format(ex.message))
            except Exception as ex:
                print "Unknown Error occured in sample_files: {}".format(ex.message)
                logging.error("ERROR: failure to read and sample '{}'".format(f))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise ValueError(
            "{} accepts 3 arguments, recieved {}".format(
                __file__,
                len(sys.argv) - 1))

    DIRECTORY = sys.argv[1]
    SAMPLES_FILE = sys.argv[3]
    PORTION = sys.argv[3]

    try:
        sample_files(DIRECTORY, SAMPLES_FILE, PORTION)
    except Exception as ex:
        print ("ERROR: Uncaught exception in sample_files " +
               "call. This shouldn't happen.")
        logging.error( ("ERROR: Uncaught exception " +
                        "in sample_files call: {}").format(ex.message))
