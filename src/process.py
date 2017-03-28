from __future__ import division

from dateutil import parser
import sys
import os
import time
import warnings
from datetime import datetime

from src import core
from src import featurize
from src import text

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split

target_encoder = LabelEncoder()

np.set_printoptions(suppress=True)



def process_date_time(df):
    def parse(ts):
        ret = ts.split(" ")
        ret.pop(4)
        return datetime.strptime(" ".join(ret), '%a %b %d %X %Y')

    start = time.time()
    sys.stdout.write("Converting to datetime...\r")
    df.created_at = df.created_at.apply(parse)
    df["day"] = df.created_at.apply(lambda x: x.day)
    df["hour"] = df.created_at.apply(lambda x: x.hour)
    print "Time to process dates: {:,.2f} seconds".format(time.time() - start)

    return df.drop('created_at', axis=1)

def process_retweet_count(df):
    start = time.time()
    sys.stdout.write("Dropping bad retweet data...\r")
    df = df[df.retweet_count.apply(lambda x: "+" not in str(x))]
    df.retweet_count = df.retweet_count.apply(int)
    print "Time to drop bad data in retweets: {:,.2f} seconds".format(time.time() - start)

    return df

def drop_extra_columns(df):
    """
    Drop useless columns that shouldn't have made it past preprocessing
    """
    sys.stdout.write("Dropping extra columns...\r")
    return df.drop(core.DROP_COLUMNS, axis=1)

def drop_null_rows(df):
    """
    EDA revealed that null rows are very uncommon, and core features always
    have corresponding null values
    """
    return df.dropna(subset=featurize.CORE_FEATURES)

def compute_and_add_target(df):
    sys.stdout.write("Adding target, tweetability...\r")
    start = time.time()

    df = df.assign(
        tweetability = df.apply(lambda x: int(x.retweet_retweet_count + featurize.TWEETABILITY_PENALTY) / \
                                (x.retweet_followers_count + 1), axis=1))

    df = df.assign(
        tweetability_metric = df.apply(lambda x: int(x.retweet_count + featurize.TWEETABILITY_PENALTY) / \
                                (x.user_followers_count + 1), axis=1))

    df.tweetability = standardize_target(df.tweetability)
    print "Time compute and add tweetability: {:,.2f} seconds".format(time.time() - start)

    return df

def standardize_target(target, transform=lambda t: StandardScaler().fit_transform(np.log(t + 1))):
    start = time.time()
    sys.stdout.write("Standardizing target...\r")

    global target_encoder

    from sklearn.cluster import KMeans

    scaled_tweetability = pd.Series(target)
    target_classified = KMeans(n_clusters=3, random_state=0).fit(
        scaled_tweetability.reshape(-1, 1))
    def stringify(v):
        if v == 0:
            return "Low"
        elif v == 1:
            return "Medium"
        elif v == 2:
            return "High"
        raise ValueError("Unexpected tweetability partition: {}".format(v))

    target = map(stringify, target_classified.labels_)

    target_encoder.fit(target)
    target =  target_encoder.transform(target)

    print "Time to standardize target: {:,.2f} seconds".format(
        time.time() - start)

    return target

def drop_none_retweets(df):
    return df[~pd.isnull(df.retweet_id_str)]

def standardize_counts(df):
    df = df.copy()
    start = time.time()
    sys.stdout.write("Standardizing measures...\r")
    minscaler = MinMaxScaler(feature_range=(0,1))
    stdscaler = StandardScaler()
    scaler = minscaler

    feats = featurize.BASE_FEATURES

    def _std(c):
        return scaler.fit_transform(np.log(c + 1))

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        df[feats] = df[feats].apply(_std)

    print "Time to standardize counts: {:,.2f} seconds".format(
        time.time() - start)

    return df

def process_df(df):
    original_size = df.size

    start = time.time()

    df = drop_none_retweets(df)
    df = drop_extra_columns(df)
    df = drop_null_rows(df)
    df = process_date_time(df)
    df = process_retweet_count(df)
    df = standardize_counts(df)
    df = text.process_text_attributes(df)

    # add target
    df = compute_and_add_target(df)

    # stuff that requires target
    print "Finished processing after {:,.2f} minutes".format((time.time() - start) / 60)
    print "DataFrame size reduced by {:.2f}%".format((1-(df.size / float(original_size)))*100)

    return df

def process_file(filename):
    filename = os.path.abspath(filename)
    outfile = os.path.join(os.path.dirname(filename),
                           "processed_" + os.path.basename(filename))

    if filename == outfile:
        raise ValueError("ERROR: filename and outfile are identical.")

    df = core.read_csv(filename)

    df = process_df(df)

    core.to_csv(df, outfile)

    file_base = outfile.split(".csv")[0]
    print "Creating train and test sets..."
    process_train_and_test(df, file_base)

    print "Done."

def produce_train_and_test(df):
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop("tweetability", axis=1), df.tweetability)
    y_train = pd.DataFrame(y_train, columns=[y_train.name])
    y_test = pd.DataFrame(y_test, columns=[y_test.name])

    return [X_train, X_test, y_train, y_test]

def write_train_and_test(fname, X_train, X_test, y_train, y_test):
    print "Writing to files under '{}' prefix".format(fname)

    filename = fname +  "_X_train.csv"
    core.to_csv(X_train, filename)

    filename = fname +  "_X_test.csv"
    core.to_csv(X_test, filename)

    filename = fname +  "_y_train.csv"
    core.to_csv(y_train, filename)

    filename = fname +  "_y_test.csv"
    core.to_csv(y_test, filename)


def process_train_and_test(df, outfile_basename):
    write_train_and_test(outfile_basename, *produce_train_and_test(df))
