from __future__ import division

import time

import numpy as np
from sklearn import tree
import matplotlib.pyplot as plt

from src import featurize
from src import core
from src import process

import pandas as pd

# this rU flag is some fix I found at https://github.com/pandas-dev/pandas/issues/11166
df = core.read_csv("data/processed_toy_sample_tweets.csv")

X_train = core.read_csv("data/processed_toy_sample_tweets_X_train.csv")
y_train = core.read_csv("data/processed_toy_sample_tweets_y_train.csv")
X_test = core.read_csv("data/processed_toy_sample_tweets_X_test.csv")
y_test = core.read_csv("data/processed_toy_sample_tweets_y_test.csv")

#
# off the cuff feature dropping
#
X_train = X_train[featurize.CORE_FEATURES]
X_test = X_test[featurize.CORE_FEATURES]


clf = tree.DecisionTreeRegressor()
start = time.time()
print "Fitting decision tree..."
clf.fit(X_train, y_train)
print "Time to fit dt: {} minutes".format((start - time.time()) / 60)

outfile = tree.export_graphviz(clf, out_file='filename.dot',
                               feature_names=X.columns)

outfile.close()
