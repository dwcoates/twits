from src import core
from src import featurize

# if __name__ is not "__main__":
#     from twits.src import core

df = core.read_csv('./data/processed_small_test_sample.csv')

X_train = core.read_csv('./data/processed_small_test_sample_X_train.csv')
X_test = core.read_csv('./data/processed_small_test_sample_X_test.csv')
y_train = core.read_csv('./data/processed_small_test_sample_y_train.csv')
y_test = core.read_csv('./data/processed_small_test_sample_y_test.csv')

#
# off the cuff feature dropping
#
X_train = X_train[featurize.FEATURES]
X_test = X_test[featurize.FEATURES]

c, r = y_train.shape
y_train = y_train.as_matrix().reshape(c,)
c, r = y_test.shape
y_test = y_test.as_matrix().reshape(c,)
