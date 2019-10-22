#!/usr/bin/env python3

import io
import ctypes
import sys
from datetime import datetime

class EnvdataStructure(ctypes.Structure):
    _fields_ = (
               ('ts', ctypes.c_double),
               ('temp', ctypes.c_double),
               ('pres', ctypes.c_double),
               ('humd', ctypes.c_double)
    )
    def __str__(self):
        s = str(self.date()) + ','
        s += str(self.temp) + ','
        s += str(self.pres) + ','
        s += str(self.humd)
        return s
    def date(self):
        return datetime.fromtimestamp(self.ts)
    def getDict(self):
        return { 'ts': self.ts,
                 'date': {
                     'default': str(self.date()),
                     'short': self.date().strftime('%m-%d %H:%M')
                 },
                 'temp': self.temp,
                 'pres': self.pres,
                 'humd': self.humd }

class EnvdataBin:
    sizeofEnvdata = ctypes.sizeof(EnvdataStructure)
    def __init__(self, filename, mode='rb'):
        if 'b' not in mode:
            mode += 'b'
        self.bf = open(filename, mode)
        self.size = int(self.bf.seek(0, 2) / self.sizeofEnvdata)
        self.bf.seek(0)
    def __del__(self):
        self.bf.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.bf.close()

    def seek(self, offset, whence=0):
        return self.bf.seek(offset * self.sizeofEnvdata, whence)
    def tell(self):
        return int(self.bf.tell() / self.sizeofEnvdata)

    def write(self, ts, temp, pres, humd):
        self.bf.write(EnvdataStructure(ts, temp, pres, humd))

    def read(self, n=None):
        if n is not None:
            self.seek(n, 2 if n < 0 else 0)
        bs = self.bf.read(self.sizeofEnvdata)
        if not bs:
            return None
        ret = EnvdataStructure()
        bs = io.BytesIO(bs)
        bs.readinto(ret)
        return ret

    def readAll(self):
        for d in iter(lambda: self.read(), None):
            yield d

    def readRange(self, rnfrom, rnto):
        if rnfrom is None:
            rnfrom = 0
        elif rnfrom < 0:
            rnfrom += self.size
        if rnto is None:
            rnto = self.size
        elif rnto < 0:
            rnto += self.size
        self.seek(rnfrom)
        for i in range(rnfrom, rnto):
            yield self.read()

    def readTsRange(self, tsfrom, tsto):
        rnfrom = None if tsfrom is None else self.binarySearch(tsfrom)[1]
        rnto = None if tsto is None else self.binarySearch(tsto)[0]
        if rnfrom is not None and rnto is not None and rnto < rnfrom:
            return
        if rnto is not None:
            rnto += 1
        yield from self.readRange(rnfrom, rnto)

    def bindData(*args):
        binded = []
        for b in args:
            binded.extend(b)
        binded.sort(key=lambda x: x.ts)
        return binded

    def binarySearch(self, ts, rn=None):
        if rn is None:
            rn = (0, self.size - 1)
        if rn[1] < rn[0]:
            return (rn[1], rn[0])
        mi = rn[0] + int((rn[1] - 1 - rn[0]) / 2)
        md = self.read(mi)
        if ts < md.ts:
            return self.binarySearch(ts, (rn[0], mi - 1))
        elif md.ts < ts:
            return self.binarySearch(ts, (mi + 1, rn[1]))
        else:
            return (mi, mi)


if __name__ == '__main__':
    with EnvdataBin(sys.argv[1], 'rb') as f:
        data = f.readRange(-10, None)
        for d in data:
            print(str(d))
