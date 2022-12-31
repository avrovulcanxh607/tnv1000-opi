#!/usr/bin/env python3

# Teletext Stream FIFO manager for VBIT hardware
# Copyright (c) 2018 Peter Kwan
# MIT License.

# What does the Fifo do?
# It takes a field of teletext data (45 byte packets, 16 line) 720 bytes
# and transfers it to the fifo
# All this module does is set up the spiram so it is ready to transfer data
#

#import OPi.GPIO as GPIO
from spi import SPIRAM
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(25, GPIO.OUT) # GPIO_MUX
class Fifo:
  def __init__(self):
    self.spiram=SPIRAM(1,0)
    self.spiram.setStatus(SPIRAM.MODE_SEQUENTIAL) #/// set the addressing mode
    #self.GPIO_MUX=25 #define GPIO_MUX 6 -> Broadcom 25
    print ('Fifo created')

  def transmit(self): #/// Read from the odd or even field and send out teletext
    #GPIO.output(self.GPIO_MUX, GPIO.LOW) # Switch the MUX to the CPU
    self.spiram.setAddress(SPIRAM.READ,0)
    #GPIO.output(self.GPIO_MUX, GPIO.HIGH) # Switch the MUX to TTX out

  def fill(self): # /// Set the control to the CPU. Ready to accept data into the fifo
    #GPIO.output(self.GPIO_MUX, GPIO.LOW) # Switch the MUX to the CPU
    self.spiram.setAddress(SPIRAM.WRITE,0)
