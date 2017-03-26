import sys
import os

sys.path.insert(0, os.path.dirname(os.getcwd()))

# see features summary in org file

# Core features that may or may not need scaling


BASE_FEATURES = ["user_friends_count",
            "user_favourites_count",
            "user_statuses_count"]
TARGET_FEATURES = ["user_followers_count", "retweet_count"]
CORE_FEATURES = BASE_FEATURES + TARGET_FEATURES
DERIVED_FEATURES = ["hashtag_count",
                    "user_mentions_count",
                    "user_hashtag_freq",
                    "user_mention_freq",
                    "text_diversity",
                    "day",
                    "hour"]
FEATURES = DERIVED_FEATURES + BASE_FEATURES

TARGET = "tweetability"

TWEETABILITY_PENALTY = 1

# To be used for derivative features
USELESS_FEATURES = ["entities_user_mentions",
    "user_profile_text_color",
    "user_description",
    "user_screen_name",
    "entities_hashtags",
    "user_name",
    "text",
    "created_at"]
