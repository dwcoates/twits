"""
Preprocess json files.
"""
import json
import gzip
import io


def read_json(filename, gz=None):
    """
    Read in comma-newline delimited json files encoded in latin-1.
    """
    _io = gzip if gz.io else io

    with _io.open("./data_sample.json", encoding="latin1") as f:
        content = f.read().strip()
        parse_fails = 0
        data = []
        for line in content.split("\n"):
            line = line[:-1] # drop annoying commas after json objects
            js = None
            try:
                js = json.loads(line)
            except Exception as ex:
                parse_fails+=1
                if parse_fails and not parse_fails % 100:
                    print ("Warning: {0} json object" +
                           " parse failures ({1})").format(parse_fails,
                                                           ex.message)
            if js:
                data.append(js)
    if parse_fails:
        print "Warning: {} json object parse failures.".format(parse_fails)
    else:
        print "No parse failures while reading '{}'".format(filename)

    return data

def process_json(j):
    """
    Stuff.
    """
    pass
