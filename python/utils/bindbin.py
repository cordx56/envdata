#!/usr/bin/env python3

import sys
from envdataio import EnvdataBin

def delDuplicate(l):
    tslist = []
    return [x for x in l if x.ts not in tslist and not tslist.append(x.ts)]

data = []
for filename in sys.argv[2:]:
    with EnvdataBin(filename) as f:
        data.extend(f.readAll())

print('All data: ' + str(len(data)))
data = delDuplicate(data)
print('Duplicate deleted: ' + str(len(data)))
data.sort(key=lambda x: x.ts)

with open(sys.argv[1], 'wb') as f:
    for d in data:
        f.write(d)
