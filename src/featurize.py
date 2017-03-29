import sys
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.getcwd()))

# see features summary in org file

# Core features that may or may not need scaling


BASE_FEATURES = ["retweet_friends_count",
            "retweet_favourites_count",
            "retweet_statuses_count",]
TARGET_FEATURES = ["retweet_followers_count", "retweet_retweet_count"]
CORE_FEATURES = BASE_FEATURES + TARGET_FEATURES
DERIVED_FEATURES = ["retweet_hashtag_count",
                    "retweet_user_mentions_count",
                    "retweet_hashtag_freq",
                    "retweet_user_mention_freq",
                    "retweet_text_diversity",
                    "day",
                    "hour"]
FEATURES = DERIVED_FEATURES + BASE_FEATURES

TARGET = "tweetability"

def tweetability_penalty(t, f):
    print type(t)
    print type(f)
    (t + 1 + np.log(f)) / (f + 1/t)


# To be used for derivative features
USELESS_FEATURES = ["entities_user_mentions",
    "user_profile_text_color",
    "user_description",
    "user_screen_name",
    "entities_hashtags",
    "user_name",
    "text",
    "created_at",
    "in_reply_to_status_id",
    "in_reply_to_status_id_str",
    "in_reply_to_user_id_str",
    "in_reply_to_screen_name",
    "in_reply_to_user_id"]
