#! /usr/bin/python

# pylint: disable=bad-whitespace,star-args

"""
Preprocess json files.
"""

import logging
import sys
import os

import json
import gzip
import unicodecsv as csv

if __name__ == "__main__":
    #from twits.src import core
    import core
else:
    from src import core

logging.basicConfig(filename="../data/preprocess.log", level=logging.DEBUG)

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
        # sys.stdout.write("FAILURE_RATE: [{0}/{1}] ({2:.2f}%)".format(encode_fails,
        #                                                   len(json_lines),
        #                                                   100*(encode_fails/float(len(json_lines)))))

    return data

def csvify_json_obj(jobj, jqs=core.BASE_FEATURES):
    """
    Return the json object ``jobj`` flattened into a line of csv
    """
    BASE_PATHS   = zip(*jqs)[1]
    return [p(jobj) for p in BASE_PATHS]

def progress_bar(value=0, endvalue=1, bar_length=50, exceptions=0):
    percent = float(value) / endvalue
    arrow = '#' * int(round(percent * bar_length)-1) + '>'
    spaces = '_' * (bar_length - len(arrow))

    sys.stdout.write(
        "Processing: [{0}] {1:.2f}% | [{2:,}/{3:,}] ({4:,} exceptions)\r".format(arrow + spaces,
                                                       percent  * 100, value, endvalue, exceptions))
    sys.stdout.flush()

def process_json(filename, output_filename, gz=False, i=0, n=1, f_num=False):
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

    fnum_str = "File #{}:".format(f_num) if f_num else ""
    print "{}Reading and processing '{}'...\r".format(fnum_str, filename)
    progress_bar(i, n, exceptions=history["other_exceptions"])
    with open(output_filename, 'wb') as fout:
        tweet_writer = csv.writer(fout)
        tweet_writer.writerow(core.BASE_HEADERS) # csv header
        js = read_json(filename, gz=gz)
        # print "Processing..."
        for i, j in enumerate(js):
            jq = core.BASE_FEATURES[:]
            if "delete" in j:
                continue # ignore deletes for now
            if "scrub_geo" in j:
                continue # I don't know what "scrub_geo" is
            try:
                if "user" not in j:
                    logging.error(
                        ("Attempt to parse json object" +
                         "without 'user' key: {} with keys: {}").format(
                             j, j.keys()))
                elif j["user"]["lang"] == "en":
                    tweet_writer.writerow(csvify_json_obj(j, jqs = jq))
                    history["english_count"] += 1
                else:
                    # don't care about non-English tweets
                    pass
            except UnicodeEncodeError as ex:
                history["encode_exceptions"] += 1
                logging.warning("Encoding exception: {}".format(ex.message))
            except KeyError as ex:
                raise ex
            except ValueError as ex:
                raise ex
            except Exception as ex:
                history["other_exceptions"] += 1
                print "ERROR: Unexpected exception: {}".format(ex.message)
                logging.error("Other exception: {}".format(ex.message))

    logging.info("Finished reading '{}'...".format(filename))


# Script
if __name__ == "__main__":
    from random import choice, shuffle

    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

    if len(sys.argv) < 3:
        raise ValueError(
            "{} accepts 2 arguments, recieved {}".format(
                __file__,
                len(sys.argv) - 1))

    DATA_PATH = os.path.abspath(sys.argv[1])
    DEST_PATH = os.path.abspath(sys.argv[2])
    TEST_LIMIT = int(sys.argv[3]) if len(sys.argv) >= 4 else None

    # be careful to not delete stuff that shouldn't be deleted
    print "Delete all ***{:,}*** files in '{}' directory?".format(
        len(os.listdir(os.path.abspath(DEST_PATH))),
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

    print "Randomizing dirs..."
    VERIFY = dict(zip(dirs, range(len(dirs))))
    shuffle(dirs)

    # I suppse this can fail for a small directory
    assert VERIFY.keys() != dirs, VERIFY.keys() == set(dirs)

    file_count = 0
    for i, f in enumerate(dirs):
        f_comps = f.split(".")
        if "json" in f_comps:
            logging.info("\n[{}]:".format(i+1))
            try:
                process_json(os.path.join(DATA_PATH, f),
                             os.path.join(DEST_PATH, f_comps[0]+".csv"),
                             gz="gz" in f_comps, i=i+1, n=len(dirs), f_num=VERIFY[f])
                file_count += 1
            except Exception as ex:

                logging.error(ex.message)
                print ex.message
        else:
            print "'{}' has been skipped for processing.".format(f)


    logging.info("Processed {}/{} files".format(file_count, len(dirs)))
