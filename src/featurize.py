import sys
import os

sys.path.insert(0, os.path.dirname(os.getcwd()))

# see features summary in org file

# Core features that may or may not need scaling
CORE_FEATURES = ["user_friends_count",
     "user_favourites_count",
     "user_statuses_count",
     "user_followers_count",
     "tweetability",
     "retweet_count"]

# To be used for derivative features
BASE_FEATURES = ["entities_user_mentions",
    "user_profile_text_color",
    "user_description",
    "user_screen_name",
    "entities_hashtags",
    "user_name",
    "text",
    "created_at"]
