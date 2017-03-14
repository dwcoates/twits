#! /usr/bin/python

"""
Preprocess json files.
"""

import logging

import json
import gzip
import io

logging.basicConfig(filename="preprocess.log", level=logging.DEBUG)

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


def process_json(filename):
    """
    Process json.
    """
    attrs = ["total_fails, total_parses, total_deletes"]
    hist = dict(zip(attrs, [0] * len(attrs)))

    logging.info("Reading '{}'...".format(filename))
    for i, j in enumerate(read_json(filename, gz=True)):
        try:
            if "delete" in j:
                history["total_deletes"] += 1
            elif j["user"]["lang"] is "en":
                out = out_line(j["id_str"],
                               j["retweeted"],
                               j["created_at"],
                               j["user"]["id_str"],
                               j["user"]["friends_count"],
                               j["user"]["lang"],
                               j["user"]["profile_text_color"],
                               j["user"]["favourites_count"],
                               j["user"]["description"],
                               j["user"]["statuses_count"],
                               j["user"]["contributors_enabled"],
                               j["user"]["followers_count"],
                               j["user"]["screen_name"],
                               j["user"]["verified"],
                               j["user"]["notifications"],
                               j["user"]["listed_count"],
                               j["user"]["created_at"],
                               j["user"]["name"],
                               j["user"]["following"],
                               j["retweet_count"],
                               j["text"],
                               j["entities"]["hashtags"],
                               j["entities"]["urls"],
                               j["entities"]["user_mentions"],
                               j["favorited"],
                               j["created_at"],
                               j["contributors"],
                               removeCommas(job["text"]),
                               parseText(job["text"]))
                history["english_count"] += 1
                fout.write(out)
        except UnicodeEncodeError as ex:
            history["encode_exceptions"] += 1
            logging.warning("Encoding exception: {}".format(ex.message))
        except Exception:
            history["other_exceptions"] += 1
            logging.warning("Other exception: {}".format(ex.message))

    logging.warning(
        "Encode exceptions for '{}': {}".format(filename,
                                                history["encode_exceptions"]))
    logging.warning(
        "Other exceptions for '{}': {}".format(filename,
                                               history["encode_exceptions"])))
    logging.info(
        "Total deletes for '{}': {}".format(filename,
                                            history["total_deletes"]))

    fout.close()


    logging.info("Finished reading '{}'...".format(filename))



logging.info("Clearning output dir...")
clear_output_dir(dest_path) # remove data remnants

dirs = listdir(origin_path)

# max?
logging.info("Processing {} dirs...".format(len(dirs)))
for f in dirs:
    if max <= 0:
        break
    max -= 1
    history["file_count"] += 1

    process_json(dest_path+f)

    fout = open(dest_path+f[0:-3], 'w')
    fout.write(get_header())
