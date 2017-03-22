from __future__ import division

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# don't use scientific notation when printing
np.set_printoptions(suppress=True)

def pp(string):
    print pd.Series(string)

df = pd.read_csv("../data/sample_tweets.csv")

# A surprisingly small number of people have no friends
print df.user_friends_count[lambda x: x == 0].size / \
    df.user_friends_count.size

f_count = np.sort(np.array(df.user_friends_count))
print np.percentile(f_count, [0, 25, 50, 95, 100])

f_count = f_count[:int(f_count.size * 0.95)]
print f_count

# There's an interesting dip in the early amounts of
# friendship.
plt.hist(f_count, bins=100)
plt.show()
