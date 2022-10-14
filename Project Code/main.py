#!/usr/bin/env python3

import pyfirmata
import http.client
import urllib.request, urllib.parse, urllib.error
import level
import time
import temp
import gas
import tilt
import buzzer
import sys
import RPi.GPIO as GPIO

LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18



# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)

def main():
  key = "DIC0NIUCJ57C6LPM"
  #board = pyfirmata.Arduino('/dev/ttyACM0',baudrate=57600)
  #arpin = board.analog[0]
  level_sensor_pin = board.analog[0]
  gas_sensor_pin = board.analog[4]
  tilt_sensor_pin = board.get_pin('d:7:i')
  #buzzer_pin = board.get_pin('d:8:o')
  #sensor_pin = board.analog[1]
  it = pyfirmata.util.Iterator(board)  
  it.start()
  level_sensor_pin.enable_reporting()
  gas_sensor_pin.enable_reporting()
  tilt_sensor_pin.enable_reporting()
  
  #sensor_pin.enable_reporting()
  
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  
  lcd_init()

  #level_val = level.sense_level(board,level_sensor_pin)
  while True:
    gas_val = gas.sense_gas(board,gas_sensor_pin) * 1000
    #power_pin.write(1)
    level_val = level.sense_level(board,level_sensor_pin)*1000
    #power_pin.write(0)
    tem,hum = temp.sense_temp_humidity()
    tilt_val = tilt.sense_tilt(board,tilt_sensor_pin)
    print(tilt_val)
    if tilt_val==1:
      buzzer.alert_buzz()
  
    lper = "LOW"
    print(level_val)
    if level_val>=590 and level_val<650:
      lper = "MEDIUM"
    elif level_val>=650:
      lper = "HIGH"
    print(lper)
    #print(tem,hum)
    #tem,hum = 12,23
    lcd_string("Temp = "+str(tem)+" C",LCD_LINE_1)
    lcd_string("Hum = "+str(hum)+" %",LCD_LINE_2)
    time.sleep(2)
    lcd_string("Level :  "+lper,LCD_LINE_1)
    lcd_string(" ",LCD_LINE_2)
    time.sleep(2)
    lcd_string("Gas = "+str(gas_val),LCD_LINE_1)
    time.sleep(2)
    

    params = urllib.parse.urlencode({'field1':level_val,'field2':tem,'field3':hum,'field4':gas_val,'field5':tilt_val,'key':key})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
      conn.request("POST", "/update", params, headers)
      response = conn.getresponse()
      data = response.read()
      conn.close()
    except:
      print ("connection failed")


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)



  


if __name__ == '__main__':

  try:
    main()
  except:
    print("Main Program stopped")
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Maintenance!",LCD_LINE_1)
    GPIO.cleanup()
    board.exit()
    it = None
    time.sleep(3)
    sys.exit(0)
    






