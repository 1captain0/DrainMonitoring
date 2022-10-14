#!/usr/bin/env python3


import sys
import Adafruit_DHT
import time


def sense_temp_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #print(('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)))
    if temperature==None or humidity==None:
        return 0,0
    else:
        return temperature,humidity


    
