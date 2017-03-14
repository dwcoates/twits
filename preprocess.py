#! /usr/bin/python

"""
Preprocess json files.
"""

import logging
import sys
import os

import json
import gzip
import csv

logging.basicConfig(filename="preprocess.log", level=logging.DEBUG)

# feature csv names with corresponding json paths
FEATURES = {"id_str":                    lambda d: d["id_str"],
            "retweeted":                 lambda d: d["retweeted"],
            "created_at":                lambda d: d["created_at"],
            "user_id_str":               lambda d: d["user"]["id_str"],
            "user_friends_count":        lambda d: d["user"]["friends_count"],
            "user_lang":                 lambda d: d["user"]["lang"],
            "user_profile_text_color":   lambda d: d["user"]["profile_text_color"],
            "user_favourites_count":     lambda d: d["user"]["favourites_count"],
            "user_description":          lambda d: d["user"]["description"],
            "user_statuses_count":       lambda d: d["user"]["statuses_count"],
            "user_contributors_enabled": lambda d: d["user"]["contributors_enabled"],
            "user_followers_count":      lambda d: d["user"]["followers_count"],
            "user_screen_name":          lambda d: d["user"]["screen_name"],
            "user_verified":             lambda d: d["user"]["verified"],
            "user_notifications":        lambda d: d["user"]["notifications"],
            "user_listed_count":         lambda d: d["user"]["listed_count"],
            "user_created_at":           lambda d: d["user"]["created_at"],
            "user_name":                 lambda d: d["user"]["name"],
            "user_following":            lambda d: d["user"]["following"],
            "retweet_count":             lambda d: d["retweet_count"],
            "text":                      lambda d: d["text"],
            "entities_hashtags":         lambda d: d["entities"]["hashtags"],
            "entities_urls":             lambda d: d["entities"]["urls"],
            "entities_user_mentions":    lambda d: d["entities"]["user_mentions"],
            "favorited":                 lambda d: d["favorited"],
            "created_at":                lambda d: d["created_at"],
            "contributors":              lambda d: d["contributors"]}

def read_json(filename, gz=None):
    """
    Read in comma-newline delimited json files encoded in latin-1.
    Use the gz flag to signify that the filename is a gzip file.

    ``something``
    """

    _open = gzip.open if gz else open

    with _open(filename) as f:
        content = f.read().decode("latin1")
        content = content.strip()
        parse_fails = 0
        data = []
        for line in content.split(",\n"):
            js = None
            try:
                js = json.loads(line)
            except Exception as ex:
                parse_fails+=1
                if parse_fails and not parse_fails % 100:
                    print ("WARNING: {0} json object " +
                           "parse failures ({1})").format(parse_fails,
                                                           ex.message)
            if js:
                data.append(js)

    if parse_fails:
        print ("WARNING: {} json object" +
               "parse failures while reading '{}'.").format(parse_fails,
                                                            filename)
    else:
        print "No parse failures while reading '{}'".format(filename)

    return data

def csvify_json_obj(jobj):
    """
    Return the json object ``jobj`` flattened into a line of csv
    """
    return map(lambda p: p(jobj), FEATURES.values())

def process_json(filename, output_filename, gz=False):
    """
    Process json.
    """

    props = ["total_fails",
             "total_parses",
             "english_count",
             "encode_exceptions",
             "other_exceptions"]
    history = dict(zip(props, [0] * len(props)))

    logging.info("Reading '{}'...".format(filename))

    with open(output_filename, 'rb') as fout:
        tweet_writer = csv.writer(fout)
        tweet_writer.writerow(FEATURES.keys()) # csv header
        for i, j in enumerate(read_json(filename, gz=gz)):
            try:
                if "delete" in j:
                    pass # ignore deletes for now
                elif j["user"]["lang"] == "en":
                    tweet_writer.writerow(csvify_json_obj(j))
                    history["english_count"] += 1
                else:
                    pass # don't care about non-English tweets
            except UnicodeEncodeError as ex:
                history["encode_exceptions"] += 1
                logging.warning("Encoding exception: {}".format(ex.message))
            except KeyError as ex:
                raise ex
            except Exception as ex:
                history["other_exceptions"] += 1
                logging.error("Other exception: {}".format(ex.message))

            logging.warning(
                "Encode exceptions for '{}': {}".format(
                    filename, history["encode_exceptions"]))
            logging.warning(
                "Other exceptions for '{}': {}".format(
                    filename, history["encode_exceptions"]))

    logging.info("Finished reading '{}'...".format(filename))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError(
            "{} accepts 2 arguments, recieved {}".format(
                __file__,
                len(sys.argv) - 1))

    dest_path = sys.argv[2]
    data_path = sys.argv[1]

    print os.listdir(data_path)

    logging.info("Clearning output dir...")

    clear_output_dir(dest_path) # remove data remnants

    # dirs = listdir(origin_path)

    # # max?
    # logging.info("Processing {} dirs...".format(len(dirs)))
    # for f in dirs:
    #     if max <= 0:
    #         break
    #     max -= 1
    #     history["file_count"] += 1
    #     process_json(dest_path+f)
    #     fout = open(dest_path+f[0:-3], 'w')
    #     fout.write(get_header())
