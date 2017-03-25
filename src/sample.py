#!/usr/bin/python
import os
import time
import unicodecsv as csv
import sys
import logging

import pandas as pd

sys.path.insert(0, os.path.dirname(os.getcwd()))

from twits.src import core

logging.basicConfig(filename="data/sample.log", level=logging.DEBUG)


def sample_rows_broken(filename, portion):
    """
    Sample a some number of rows of ``filename`` according to ``portion``,
    which is a number between 0 and 1 indicating the percentage of rows to
    randomly sample *without* replacement.
    """

    df = core.read_csv(filename)

    num_samples = int(len(df.index) * portion)

    return df.sample(n = num_samples).to_records()

def sample_rows(df, portion):
    """
    Sample a some number of rows of ``filename`` according to ``portion``,
    which is a number between 0 and 1 indicating the percentage of rows to
   randomly sample *without* replacement.
    """
    num_samples = int(len(df.index) * portion)

    return df.sample(n = num_samples)

def sample_files_broken(directory, output_filename, portion):
    """
    Return a dataframe constructed from a portion of all csv files in
    directory.
    """

    DATA_DIR = os.path.abspath(directory)
    FILES = os.listdir(DATA_DIR)
    FILENAME = os.path.basename(output_filename)
    OUTPUT_FILE = os.path.join(os.path.dirname(DATA_DIR), os.path.basename(FILENAME))

    #sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    with open(OUTPUT_FILE, 'wb') as fout:
        sample_writer = csv.writer(fout)
        sample_writer.writerow(core.BASE_HEADERS)
        for i, f in enumerate(FILES):
            if "csv" != f.split(".")[-1]:
                print "Skipping '{}' for sampling.".format(f)
                continue
            try:
                rows = sample_rows(os.path.join(DATA_DIR, f), portion)
                for i, row in enumerate(rows):
                    if len(row)-1 == len(core.BASE_HEADERS):
                        sample_writer.writerow(row)
                    else:
                        msg = "Row #{} from '{}' has {} elements. It should have {}"
                        raise ValueError(msg.format(i+1, f, len(row)-1, len(core.BASE_HEADERS)))
                sys.stdout.flush()
                sys.stdout.write('{}\r'.format("\033[95mSampled from:\033[0m [{}/{}]".format(i+1, len(FILES))))
            except ValueError as ex:
                print "WARNING: {}".format(ex.message)
                logging.warn("WARNING: {}".format(ex.message))
            except Exception as ex:
                print "Unknown Error occured in sample_files: {}".format(ex.message)
                logging.error("ERROR: failure to read and sample '{}'".format(f))
    sys.stdout.write( "Done.")

def sample_files(directory, output_filename, portion):
    """
    This seems to correct a write bug introduced by sample_files. My only
    concern is that it will cause memories errors for large samples, and in
    general be very slow. Oh well.
    NOTE: interesting, doesn't seem to have slowed down process time.
    """

    DATA_DIR = os.path.abspath(directory)
    FILES = os.listdir(DATA_DIR)
    FILENAME = os.path.basename(output_filename)
    OUTPUT_FILE = os.path.join(os.path.dirname(DATA_DIR), os.path.basename(FILENAME))

    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    df = None
    for i, f in enumerate(FILES):
        if "csv" != f.split(".")[-1]:
            print "Skipping '{}' for sampling.".format(f)
            continue
        try:
            new_df = core.read_csv(os.path.join(DATA_DIR, f))
            new_df = sample_rows(df, portion)
            df = pd.concat([df, new_df]) if df is not None else new_df
            sys.stdout.flush()
            sys.stdout.write('{}\r'.format("\033[95mSampled from:\033[0m [{}/{}]".format(i+1, len(FILES))))
        except ValueError as ex:
            print "WARNING: {}".format(ex.message)
            logging.warn("WARNING: {}".format(ex.message))
        except Exception as ex:
            print "Unknown Error occured in sample_files: {}".format(ex.message)
            logging.error("ERROR: failure to read and sample '{}'".format(f))
    core.to_csv(df, OUTPUT_FILE)
    sys.stdout.write( "Done.")


# Script
if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise ValueError(
            "{} accepts 3 arguments, recieved {}".format(
                __file__,
                len(sys.argv) - 1))

    DIRECTORY = sys.argv[1]
    SAMPLES_FILE = sys.argv[2]
    PORTION = float(sys.argv[3])

    try:
        sample_files2(DIRECTORY, SAMPLES_FILE, PORTION)
    except Exception as ex:
        print ("ERROR: Uncaught exception in sample_files " +
               "call. This shouldn't happen.")
        logging.error( ("ERROR: Uncaught exception " +
                        "in sample_files call: {}").format(ex.message))
