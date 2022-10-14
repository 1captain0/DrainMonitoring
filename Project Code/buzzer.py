#!/usr/bin/env python3

import pyfirmata
import math
import time

board = pyfirmata.Arduino("/dev/ttyACM0")
SENSOR_PIN = 1
PIEZO_PIN = board.get_pin('d:8:o')
it = pyfirmata.util.Iterator(board)
it.start()

board.analog[SENSOR_PIN].enable_reporting()


def alert_buzz():
  try:
    PIEZO_PIN.write(0)
    for i in range(5):
      PIEZO_PIN.write(1)
      time.sleep(0.5)
      PIEZO_PIN.write(0.8)
      time.sleep(0.5)
    PIEZO_PIN.write(0)
    return
  except:
    print("Stopped Buzzer")
    
