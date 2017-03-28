from src import core

# if __name__ is not "__main__":
#     from twits.src import core

df = core.read_csv('./data/processed_toy_sample_tweets.csv')

X_train = core.read_csv('./data/processed_toy_sample_tweets_X_train.csv')
y_test = core.read_csv('./data/processed_toy_sample_tweets_X_test.csv')
X_train = core.read_csv('./data/processed_toy_sample_tweets_y_train.csv')
y_test = core.read_csv('./data/processed_toy_sample_tweets_y_test.csv')
