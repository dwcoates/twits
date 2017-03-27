import pandas as pd
import io
import time

import matplotlib
matplotlib.use("qt4agg")
from matplotlib import pyplot as plt

from src import core

# defunct
start = time.time()
print "reading data..."
data = io.open("./data_sample.json",
               encoding='latin-1').read().strip()
data_time = time.time() - start
print "Time to read data: {:.2f} seconds".format(data_time)

data = "[" + data[:-1] + "]"  # can forget this

start = time.time()
df = pd.read_json(data)
df_time = time.time() - start
print "Time to create dataframe: {:.2f} seconds".format(df_time)
print "dataframe creation is {:.2f} times slower than reading.".format(
    df_time / float(data_time))

dfn = df.dropna(subset = ["text"])

lengths = dfn.apply(lambda x: len(x.text), axis=1)

fig = plt.figure(1, figsize = (8.5,11))
fig.suptitle('Tweet text length distribution')
plt.xlim((0,150))
plt.hist(lengths, bins=300)
plt.show()

fig = plt.figure(1, figsize = (8.5,11))
fig.suptitle('Retweet length distribution')
plt.xlim((0,1000))
plt.hist(dfn[dfn.retweet_count > 100].retweet_count.values, bins=200)
plt.show()
