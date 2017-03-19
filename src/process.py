from __future__ import division

from dateutil import parser
import sys
import time

import pandas as pd
import numpy as np

def process_file(filename):
    sys.stdout.flush()
    sys.stdout.write("Processing '{}'\r".format(filename))
    start = time.time()
    sys.stdout.write("Reading...\r")
    df = pd.read_csv(filename)
    print "Time to read: {:,.2f} seconds".format(time.time() - start)

    start = time.time()
    sys.stdout.write("Converting to datetime...\r")
    df.created_at = df.created_at.apply(lambda x: parser.parse(x))
    print "Time to read: {:,.2f} minutes".format((time.time() - start) / 60)

    print "Done."

    return df
