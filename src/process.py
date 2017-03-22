from __future__ import division

from dateutil import parser
import sys
import os
import time
import warnings
from datetime import datetime

sys.path.insert(0, '/home/dodge/workspace/twits/src')

import core

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

def process_date_time(df):
    def parse(ts):
        ret = ts.split(" ")
        ret.pop(4)
        return datetime.strptime(" ".join(ret), '%a %b %d %X %Y')


    start = time.time()
    sys.stdout.write("Converting to datetime...\r")
    df.created_at = df.created_at.apply(parse)
    print "Time to process dates: {:,.2f} minutes".format((time.time() - start) / 60)

    return df

def read_csv(filename):
    # Reading
    start = time.time()
    sys.stdout.write("Reading...\r")
    df = pd.read_csv(filename)
    print "Time to read: {:,.2f} seconds".format(time.time() - start)

    return df

def process_retweet_count(df):
    start = time.time()
    sys.stdout.write("Dropping bad retweet data...\r")
    df = df[df.retweet_count.apply(lambda x: "+" not in str(x))]
    print "Time to drop bad data in retweets: {:,.2f} minutes".format((time.time() - start) / 60)

    return df

def drop_extra_columns(df):
    """
    Drop useless columns that shouldn't have made it past preprocessing
    """
    return df.drop(core.DROP_COLUMNS, axis=1)

def compute_and_add_target(df):
    return df.assign(tweetability = df.retweet_count / df.user_followers_count)

def add_log_transforms(df):
    """
    Should be called last
    """
    COLUMNS   = ["user_friends_count",
                 "user_favourites_count",
                 "user_statuses_count",
                 "user_followers_count",
                 "user_listed_count",
                 "retweet_count",
                 "tweetability"]


    return df

def process_df(df):
    original_size = df.size

    start = time.time()

    df = process_date_time(df)
    df = process_retweet_count(df)
    df = drop_extra_columns(df)
    df = add_log_transforms(df)

    # add target
    df = compute_and_add_target(df)

    print "Finished processing after {:,.2f} minutes".format((time.time() - start) / 60)
    print "DataFrame size reduced by {:.2f}%".format((1-(df.size / float(original_size)))*100)

    return df

def process_file(filename, outfile):

    sys.stdout.write("Reading '{}'...\r".format(os.path.abspath(filename)))
    df = read_csv(filename)
    sys.stdout.flush()

    df = process_df(df)
    sys.stdout.write("Writing '{}'...\r".format(os.path.abspath(outfile)))
    with open(outfile, 'wb') as fout:
        df.to_csv(fout, encoding="utf8")

    print "Done."

    return df

def produce_train_and_test(df):
    X_train, X_test, y_train, y_test = train_test_split(df.drop("tweetability", axis=1), df.tweetability)

    return [X_train, X_test, y_train, y_test]

def write_train_and_test(fname, X_train, X_test, y_train, y_test):
    print "Writing to '{}'".format(fname)

    X_train.to_csv(fname +  "_X_train.csv", encoding="utf8")
    X_test.to_csv(fname +  "_X_test.csv", encoding="utf8")
    y_train.to_csv(fname +  "_y_train.csv", encoding="utf8")
    y_test.to_csv(fname +  "_y_test.csv", encoding="utf8")

    return None

def process_train_and_test(df, outfile_basename):
    write_train_and_test(outfile_basename, *produce_train_and_test(df))

    return None

# unused
def standardize_counts(df):
    start = time.time()
    sys.stdout.write("Standardizing measures...\r")
    minscaler = MinMaxScaler(feature_range=(-1,1))
    stdscaler = StandardScaler()

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        df[core.CORE_FEATURES] = df[core.CORE_FEATURES].apply(lambda c: stdscaler.fit_transform(pd.to_numeric(c)))

    print "Time to standardize: {:,.2f} minutes".format((time.time() - start) / 60)

    return df
