#!/usr/bin/env python3

import pyfirmata
import time


def sense_gas(board,pin):
    try:
    #arpin = board.analog[0]
        pin.enable_reporting()
        lev = pin.read()
        if lev!=None:
            return lev
        else:
            pass
        #time.sleep(1)
    except:
        print("Stopped gas sensor")

