#! /usr/bin/python

# pylint: disable=bad-whitespace,star-args

"""
Preprocess json files.
"""

import logging
import sys
import os
import re
import codecs

import json
import gzip
import csv

logging.basicConfig(filename="preprocess.log", level=logging.DEBUG)


ESCAPE_SEQUENCE_RE = re.compile(r"""
     \\U........
    | \\u....
    | \\x..
    | \\[0-7]{1,3}
    | \\N\{[^}]+\}
    | \\[\\'\\"abfnrtv]
    """, re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


# feature csv names with corresponding json paths
FEATURES = [("id_str",                    lambda d: d["id_str"]),
            ("retweeted",                 lambda d: d["retweeted"]),
            ("created_at",                lambda d: d["created_at"]),
            ("user_id_str",               lambda d: d["user"]["id_str"]),
            ("user_friends_count",        lambda d: d["user"]["friends_count"]),
            ("user_lang",                 lambda d: d["user"]["lang"]),
            ("user_profile_text_color",   lambda d: d["user"]["profile_text_color"]),
            ("user_favourites_count",     lambda d: d["user"]["favourites_count"]),
            ("user_description",          lambda d: d["user"]["description"]),
            ("user_statuses_count",       lambda d: d["user"]["statuses_count"]),
            ("user_contributors_enabled", lambda d: d["user"]["contributors_enabled"]),
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
            ("entities_hashtags",         lambda d: d["entities"]["hashtags"]),
            ("entities_urls",             lambda d: d["entities"]["urls"]),
            ("entities_user_mentions",    lambda d: d["entities"]["user_mentions"]),
            ("favorited",                 lambda d: d["favorited"]),
            ("created_at",                lambda d: d["created_at"]),
            ("contributors",              lambda d: d["contributors"])]
HEADERS = zip(*FEATURES)[0]
PATHS   = zip(*FEATURES)[1]

def read_json(filename, gz=None):
    """
    Read in comma-newline delimited json files encoded in latin-1.
    Use the gz flag to signify that the filename is a gzip file.

    ``something``
    """

    _open = gzip.open if gz else open

    parse_fails = 0
    with _open(filename) as f:
        content = f.read().decode("raw_unicode_escape")
        content = content.strip()[:-3]
        json_lines = content.split(",\n")
        data = []
        encode_fails = 0
        for i, line in enumerate(json_lines):
            try:
                data.append(json.loads(line))
            except ValueError as ex:
                encode_fails += 1
            except Exception:
                print "JSON OBJECT FAILED:".format(i)
        logging.warning("FAILURE_RATE: [{0}/{1}] ({2:.2f}%)".format(encode_fails,
                                                                    len(json_lines),
                                                                    100*(encode_fails/float(len(json_lines)))))

    return data

def csvify_json_obj(jobj):
    """
    Return the json object ``jobj`` flattened into a line of csv
    """
    return [p(jobj) for p in PATHS]

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

    with open(output_filename, 'wb') as fout:
        tweet_writer = csv.writer(fout)
        tweet_writer.writerow(HEADERS) # csv header
        print "Reading '{}'...".format(filename)
        js = read_json(filename, gz=gz)
        print "Processing...".format(filename)
        for i, j in enumerate(js):
            if "delete" in j:
                continue # ignore deletes for now
            if "scrub_geo" in j:
                continue # I don't know what "scrub_geo" is
            try:
                if "user" not in j:
                    logging.error(
                        ("Attempt to parse json object" +
                         "without 'user' key: {} with keys: {}").format(j,
                                                                        j.keys()))
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
            except ValueError as ex:
                raise ex
            except Exception as ex:
                history["other_exceptions"] += 1
                logging.error("Other exception: {}".format(ex.message))

            logging.warning(
                "Encode exceptions: {}".format(
                    filename, history["encode_exceptions"]))
            logging.warning(
                "Other exceptions: {}".format(
                    filename, history["encode_exceptions"]))

    logging.info("Finished reading '{}'...".format(filename))


# Script
if __name__ == "__main__":
    from random import choice

    if len(sys.argv) < 3:
        raise ValueError(
            "{} accepts 2 arguments, recieved {}".format(
                __file__,
                len(sys.argv) - 1))


    DEST_PATH = os.path.abspath(sys.argv[2])
    DATA_PATH = os.path.abspath(sys.argv[1])

    TEST_LIMIT = int(sys.argv[3]) if len(sys.argv) >= 4 else None

    # be careful to not delete stuff that shouldn't be deleted
    print "Delete all files in '{}' directory?".format(
        os.path.abspath(DEST_PATH))
    INPUT = raw_input("yes or no> ")
    if INPUT != "yes":
        exit()

    # delete files in destination directory
    logging.info("Clearing output dir...")
    for f in os.listdir(DEST_PATH):
        os.remove(os.path.join(DEST_PATH, f))

    dirs = os.listdir(DATA_PATH)

    if len(dirs) == 0:
        raise ValueError("data directory '{}' is empty.".format(DATA_PATH))

    logging.info("Processing {} dirs...".format(len(dirs)))

    if TEST_LIMIT:
        dirs = [choice(dirs) for _ in xrange(TEST_LIMIT)]

    file_count = 0
    for i, f in enumerate(dirs):
        f_comps = f.split(".")
        if "json" in f_comps:
            print "\n[{}/{}]".format(i+1, len(dirs))
            try:
                process_json(os.path.join(DATA_PATH, f),
                             os.path.join(DEST_PATH, f_comps[0]+".csv"),
                             gz="gz" in f_comps)
                file_count += 1
            except Exception as ex:
                logging.error(ex.message)
                print ("ERROR: Failed to processes" +
                       " '{}' in '{}' to '{}'.").format(f,
                                                        DATA_PATH,
                                                        DEST_PATH)
        else:
            print "'{}' has been skipped for processing.".format(f)


    logging.info("Processed {}/{} files".format(file_count, len(dirs)))
