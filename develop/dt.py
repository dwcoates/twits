from __future__ import division

import time

import numpy as np
from sklearn import tree
import matplotlib.pyplot as plt

from src import featurize
from src import core
from src import process

import pandas as pd

from sklearn.metrics import accuracy_score, log_loss
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedKFold

# this rU flag is some fix I found at https://github.com/pandas-dev/pandas/issues/11166
df = core.read_csv("data/processed_toy_sample_tweets.csv")

X_train = core.read_csv("data/processed_toy_sample_tweets_X_train.csv")
y_train = core.read_csv("data/processed_toy_sample_tweets_y_train.csv")
X_test = core.read_csv("data/processed_toy_sample_tweets_X_test.csv")
y_test = core.read_csv("data/processed_toy_sample_tweets_y_test.csv")

#
# off the cuff feature dropping
#
X_train = X_train[featurize.FEATURES]
X_test = X_test[featurize.FEATURES]

pipe_lr = Pipeline([('scl', StandardScaler()), ('clf', LogisticRegression(random_state=1))])
pipe_lr.fit(X_train, y_train)

kfold = StratifiedKFold(y=y_train, n_folds=10, random_state=1)
scores = []

for k, (train, test) in enumerate(kfold):
    pipe_lr.fit(X_train[train], y_train[train])
    score = pipe_lr.score(X_train[test], y_train[test])
    scores.append(score)
    print 'Fold: {}, Class dist.: {}, Acc: {:.3f}'.format(k+1,
                                                          np.bincount(y_train[train]),
                                                          score)


#
# Simple Decision Tree Regressor
#
clf = tree.DecisionTreeClassifier()
start = time.time()
print "Fitting decision tree..."
clf.fit(X_train, y_train)
print "Time to fit dt: {} minutes".format((start - time.time()) / 60)

outfile = tree.export_graphviz(clf, out_file='filename.dot',
                               feature_names=X_train.columns)

#
# Random Forest Regressor
#
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators=1000, random_state=0, n_jobs=4)
forest.fit(X_train, y_train)

clf1 = LogisticRegression(random_state=1)
clf2 = RandomForestClassifier(random_state=1)
clf3 = GaussianNB()

eclf1 = VotingClassifier(estimators=[
        ('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')
eclf1 = eclf1.fit(X_train, y_train)
pred1 = eclf1.predict(X_test)

eclf2 = VotingClassifier(estimators=[
        ('lr', clf1), ('rf', clf2), ('gnb', clf3)],
        voting='soft')
eclf2 = eclf2.fit(X_train, y_train)
pred2 = eclf2.predict(X_test)

eclf3 = VotingClassifier(estimators=[
       ('lr', clf1), ('rf', clf2), ('gnb', clf3)],
       voting='soft', weights=[2,1,1])
eclf3 = eclf3.fit(X_train, y_train)
pred3 = eclf3.predict(X_test)
