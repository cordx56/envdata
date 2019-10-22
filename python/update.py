#!/usr/bin/env python3

import sys
from smbus2 import SMBus
import bme280
from utils.envdataio import EnvdataBin

with SMBus(1) as bus:
    data = bme280.sample(bus)
    with EnvdataBin(sys.argv[1], 'ab') as f:
        f.write(data.timestamp.timestamp(), data.temperature, data.pressure, data.humidity)
