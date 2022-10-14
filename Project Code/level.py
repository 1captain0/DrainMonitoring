#!/usr/bin/env python3

import pyfirmata
import time

def sense_level(board,pin):
    try:
        #power_pin = board.get_pin('d:2:o')
        #power_pin.write(1)
        pin.enable_reporting()
        lev = pin.read()
        if lev!=None:
            return lev
        else:
            pass
        #time.sleep(1)
    except:
        print("Stopped level sensor")
