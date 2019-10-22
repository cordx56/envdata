#!/usr/bin/env python3

import sys
from envdataio import EnvdataBin

with EnvdataBin(sys.argv[1]) as f:
    for d in f.readRange(None, 10):
        print(str(d))
