"""
Core stuff
"""

import sys
import time

import pandas as pd

# feature csv names with corresponding json paths
BASE_FEATURES = [("id_str",                    lambda d: d["id_str"]),
                     ("created_at",                lambda d: d["created_at"]),
                     ("user_id_str",               lambda d: d["user"]["id_str"]),
                     ("user_friends_count",        lambda d: d["user"]["friends_count"]),
                     ("user_profile_text_color",   lambda d: d["user"]["profile_text_color"]),
                     ("user_favourites_count",     lambda d: d["user"]["favourites_count"]),
                     ("user_description",          lambda d: d["user"]["description"]),
                     ("user_statuses_count",       lambda d: d["user"]["statuses_count"]),
                     ("user_followers_count",      lambda d: d["user"]["followers_count"]),
                     ("user_screen_name",          lambda d: d["user"]["screen_name"]),
                     ("user_verified",             lambda d: d["user"]["verified"]),
                     ("user_notifications",        lambda d: d["user"]["notifications"]),
                     ("user_listed_count",         lambda d: d["user"]["listed_count"]),
                     ("user_created_at",           lambda d: d["user"]["created_at"]),
                     ("user_name",                 lambda d: d["user"]["name"]),
                     ("user_following",            lambda d: d["user"]["following"]),
                     ("retweet_count",             lambda d: d["retweet_count"]),
                     ("text",                      lambda d: d["text"]),
                     ("retweeted",                 lambda d: d["retweeted"]),
                     ("in_reply_to_status_id",     lambda d: d["in_reply_to_status_id"]),
                     ("in_reply_to_status_id_str", lambda d: d["in_reply_to_status_id_str"]),
                     ("in_reply_to_user_id_str",   lambda d: d["in_reply_to_user_id_str"]),
                     ("in_reply_to_screen_name",   lambda d: d["in_reply_to_screen_name"]),
                     ("in_reply_to_user_id",       lambda d: d["in_reply_to_user_id"]),
                     ("entities_hashtags",         lambda d: [j["text"] for j in d["entities"]["hashtags"]]),
                     ("entities_user_mentions",    lambda d: [j["screen_name"] for j in d["entities"]["user_mentions"]]),
                     ("favorited",                 lambda d: d["favorited"])]
BASE_HEADERS = zip(*BASE_FEATURES)[0]
BASE_PATHS   = zip(*BASE_FEATURES)[1]

DROP_COLUMNS = ["user_lang",
                "user_notifications",
                "user_verified",
                "user_following",
                "retweeted",
                "favorited",
                "contributors"]

CORE_FEATURES = [h for h in BASE_HEADERS if h not in DROP_COLUMNS]

CORE_FEATURES.append("tweetability") # target feature


# convenience function
def pp(lst):
    print pd.Series(lst)


# use this to read
def read_csv(filename, suppress_msg=False):
    # Reading
    start = time.time()
    if not suppress_msg:
        sys.stdout.write("Reading form '{}'...\r".format(filename))
    with open(filename, 'rU') as fout:
        df = pd.read_csv(fout, index_col=False, encoding="utf8")
    if not suppress_msg:
        print "Time to read: {:,.2f} seconds".format(time.time() - start)
        sys.stdout.flush()

    return df

# this to write
def to_csv(df, filename):
    start = time.time()
    sys.stdout.write("Writing to '{}'...\r".format(filename))
    with open(filename, 'wb') as fout:
        df.to_csv(fout, encoding="utf8", index=False)
    print "Time to write: {:,.2f} seconds".format(time.time() - start)
    sys.stdout.flush()
