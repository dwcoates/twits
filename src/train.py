from ..src import core

if __name__ is not "__main__":
    from twits.src import core

X_train = core.read_csv('./data/processed_toy_sample_tweets_X_train.csv')
y_train = core.read_csv('./data/processed_toy_sample_tweets_X_train.csv')
X_test = core.read_csv('./data/processed_toy_sample_tweets_X_train.csv')
y_test = core.read_csv('./data/processed_toy_sample_tweets_X_train.csv')
