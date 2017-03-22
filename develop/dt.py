import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from

import pandas as pd

# this rU flag is some fix I found at https://github.com/pandas-dev/pandas/issues/11166
df = pd.read_csv(open("../data/processed_sample_tweets.csv", 'rU'), encoding="utf8")

X = pd.read_csv(open("../data/processed_sample_tweets_X_train.csv", 'rU'), encoding="utf8")
y = pd.read_csv(open("../data/processed_sample_tweets_y_train.csv", 'rU'), encoding="utf8")

clf = DecisionTreeRegressor(X, y)
clf.fit()
