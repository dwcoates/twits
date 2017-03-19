from __future__ import division

from dateutil import parser
import sys
import time

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import md5, sha


def process_date_time(df):
    # Date/Time
    start = time.time()
    sys.stdout.write("Converting to datetime...\r")
    df.created_at = df.created_at.apply(lambda x: parser.parse(x))
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

def standardize_counts(df):
    start = time.time()
    sys.stdout.write("Standardizing measures...\r")
    minscaler = MinMaxScaler(feature_range=(-1,1))
    stdscaler = StandardScaler()
    columns   = ["user_friends_count",
                 "user_favourites_count",
                 "user_statuses_count",
                 "user_followers_count",
                 "user_listed_count",
                 "retweet_count"]

    df[columns] = df[columns].apply(lambda c: stdscaler.fit_transform(pd.to_numeric(c)))

    print "Time to standardize: {:,.2f} minutes".format((time.time() - start) / 60)

    return df

def process_file(filename):
    print "Processing '{}'\r".format(filename)
    start = time.time()

    df = read_csv(filename)
    df = process_date_time(df)
    df = process_retweet_count(df)
    df = standardize_counts(df)

    print "Finished processing '{}' after {:,.2f} minutes".format(filename,
                                                                  (time.time() - start) / 60)

    return df
