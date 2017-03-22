from __future__ import division

import time

import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

from src import featurize

import pandas as pd

# this rU flag is some fix I found at https://github.com/pandas-dev/pandas/issues/11166
df = pd.read_csv(open("../data/processed_sample_tweets.csv", 'rU'), encoding="utf8")

fname = "data/processed_toy_sample_tweets_X_train.csv"
print "Reading features from '{}'...".format(fname)
X = pd.read_csv(open(fname, 'rU'), encoding="utf8")

fname = "data/processed_toy_sample_tweets_y_train.csv"
print "Reading target from  '{}'...".format(fname)
y = pd.read_csv(open(fname, 'rU'), encoding="utf8")

#
# off the cuff feature dropping
#
X = X[featurize.CORE_FEATURES]

clf = DecisionTreeRegressor(X, y)
start = time.time()
print "Fitting decision tree..."
clf.fit(X, y)
print "Time to fit dt: {} minutes".format((start - time.time()) / 60)
