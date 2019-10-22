#!/usr/bin/env python3

import sys
from datetime import datetime
from envdataio import EnvdataBin

def show(bf, n):
    return str(n) + ': ' + str(bf.read(n))

print('Input like: 2019-10-14 09:55:00.0')
with EnvdataBin(sys.argv[1]) as f:
    while True:
        inputstr = input()
        try:
            n = int(inputstr)
            print(show(f, n))
        except:
            t = datetime.strptime(inputstr, '%Y-%m-%d %H:%M:%S.%f').timestamp()
            r = f.binarySearch(t)
            for i in range(2):
                if r[i] < 0:
                    print(str(r[i]) + ': range over')
                    continue
                elif f.size <= r[i]:
                    print(str(r[i]) + ': range over')
                    continue
                print(show(f, r[i]))
