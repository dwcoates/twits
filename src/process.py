from __future__ import division

from dateutil import parser
import sys
import time
import warnings
from datetime import datetime

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler


def process_date_time(df):
    def parse(ts):
        ret = ts.split(" ")
        ret.pop(4)
        return datetime.strptime(
            parse(" ".join(ret), '%a %b %d %X %Y')

    # Date/Time
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

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        df[columns] = df[columns].apply(lambda c: stdscaler.fit_transform(pd.to_numeric(c)))

    print "Time to standardize: {:,.2f} minutes".format((time.time() - start) / 60)

    return df

def drop_extra_columns(df):
    """
    Drop useless columns that shouldn't have made it past preprocessing
    """
    columns = ["created_at.1",
               "user_lang",
               "user_notifications",
               "user_verified",
               "user_following",
               "retweeted",
               "favorited",
               "contributors"]

    return df.drop(columns, axis=1)

def add_y(df):
    df.retweeted()

    return df

def process_df(df):
    df = process_date_time(df)
    df = process_retweet_count(df)
    df = standardize_counts(df)
    df = drop_extra_columns(df)

    return df

def process_file(filename):
    print "Processing '{}'\r".format(filename)
    start = time.time()

    df = process_df(read_csv(filename))

    print "Finished processing '{}' after {:,.2f} minutes".format(filename,
                                                                  (time.time() - start) / 60)

    return df
