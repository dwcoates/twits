"""
Preprocess json files.
"""
import json
import gzip
import io

import pandas as pd


def read_json(filename, gz=None):
    """
    Read in comma-newline delimited json files encoded in latin-1.
    Use the gz flag to signify that the filename is a gzip file.
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

def read_pandas(filename, gz=None):

    _io = gzip.io if gz else io

    with _io.open(filename, encoding="latin1") as f:
        s = f.read().split(",\n")

        df = pd.read_json(s)

    return df

def process_json(j):
    """
    Stuff.
    """
    pass
