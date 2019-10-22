#!/usr/bin/env python3

import sys
from datetime import datetime
from envdataio import EnvdataBin


# str(datetime.datetime.fromtimestamp(datetime.datetime.strptime('2019-10-12 20:30:01.610834', '%Y-%m-%d %H:%M:%S.%f').timestamp()))

with open(sys.argv[1], 'r') as sf:
    with EnvdataBin(sys.argv[2], 'w') as df:
        for sfline in sf:
            data = sfline.split(',')
            data[0] = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S.%f').timestamp()
            data[1] = float(data[1])
            data[2] = float(data[2])
            data[3] = float(data[3])
            df.write(ts=data[0], temp=data[1], pres=data[2], humd=data[3])
