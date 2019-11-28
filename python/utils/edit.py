#!/usr/bin/env python3

import sys
from envdataio import EnvdataBin

with EnvdataBin(sys.argv[1], "rb+") as f:
    while True:
        print("Enter command(m for help)> ", end="")
        mode = input()
        if mode == "q":
            break
        elif mode == "l":
            print(f.size)
        elif mode == "p":
            print("Print data> ", end="")
            n = int(input())
            print(str(f.read(n)))
        elif mode == "e":
            print("Edit data> ", end="")
            n = int(input())
            d = f.read(n)
            print("Time stamp(default: " + str(d.ts) + ")> ", end="")
            i = input()
            if i != "":
                d.ts = float(i)
            print("Temperature(default: " + str(d.temp) + ")> ", end="")
            i = input()
            if i != "":
                d.temp = float(i)
            print("Pressure(default: " + str(d.pres) + ")> ", end="")
            i = input()
            if i != "":
                d.pres = float(i)
            print("Humidity(default: " + str(d.humd) + ")> ", end="")
            i = input()
            if i != "":
                d.humd = float(i)
            f.seek(n)
            f.write(d.ts, d.temp, d.pres, d.humd)
        elif mode == "d":
            print("Delete data> ", end="")
            n = int(input())
            for i in range(n, f.size - 1):
                d = f.read(i + 1)
                f.seek(i)
                f.write(d.ts, d.temp, d.pres, d.humd)
            f.truncate(None)
        else:
            print("l    Print length of data")
            print("p    Print data")
            print("e    Edit data")
            print("d    Delete data")
            print("q    Quit")
