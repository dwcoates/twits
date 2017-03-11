"""
Preprocess json files.
"""

import json
import io

def read_json(filename, prefix):
    # comma-newline delimited json files
    with io.open("./data_sample.json") as f:
        content = f.read().strip().decode("utf-8")
        data = []
        for line in content:
            line = line.decode("utf8", "ignore")
            j = None
            try:
                j = json.loads(line)
            except UnicodeEncodeError as ex:
                try:
                    line = json.loads(line.encode('latin-1'))
                except Exception:
                    print "fuck"
            except Exception:
                print "hello"
            if j:
                data.append(j)
