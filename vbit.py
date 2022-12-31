#!/usr/bin/env python3

# Teletext Stream to VBIT hardware
# Copyright (c) 2018 Peter Kwan
# MIT License.

# Release 1.0.1

# System libraries
import sys
import numpy as np
import time
import OPi.GPIO as GPIO
import smbus

# Local libraries
from tnv1000 import tnv1000
from fifo import Fifo
from buffer import Buffer

# Use Broadcom pin numbering
GPIO.setmode(GPIO.BOARD)

# Globals
packetSize=42 # The input stream packet size. Does not include CRI and FC

# Setup
#tnv1000()

# Objects
fifo=Fifo()

bus=smbus.SMBus(0)

# buffer stuff
head=0
tail=0
BUFFERS = 4
buf = [0] * BUFFERS
for i in range(BUFFERS):
  buf[i]=Buffer()

countdown=BUFFERS-1
if countdown<1:
  countdown=1

GPIO_FLD=7 #define GPIO_FLD 3 -> Broadcom 22
GPIO_CSN=12 #define GPIO_CSN 5 -> Broadcom 24
#GPIO_MUX=25 #define GPIO_MUX 6 -> Broadcom 25
GPIO_LED=11 #define GPIO_LED 7 -> Broadcom 4

# setup the I/O to VBIT
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_FLD, GPIO.IN)
#GPIO.setup(18, GPIO.OUT)
#GPIO.setup(24, GPIO.OUT)

#GPIO.output(24, GPIO.LOW)
tnv1000()
#GPIO.output(24, GPIO.HIGH)
#def adv_int(self):
#  print("ADV Interrupt")

#GPIO.add_event_detect(27, GPIO.BOTH, callback=adv_int)

# This is the interrupt routine that triggers on each field
def fieldEdge(self):
  global buf
  global GPIO_LED
  global GPIO_FLD
  global tail
  global head
  GPIO.output(GPIO_LED, GPIO.LOW)
  ##### Wait until the vbi has been transmitted #####
  time.sleep(0.0016) # Between Suspend while 1.6 ms
  # vbi is done. load the next field
  fifo.spiram.deselect()
  GPIO.output(GPIO_LED, GPIO.HIGH)
  # we are done with the buffer
  if head == tail: # Source buffer was not ready. We're going to need a faster Pi.
    print ('?') 
  ##### Copy from the source buffer to the fifo #####
  fifo.fill()
  arr=buf[tail].field.reshape(720).tobytes()
  fifo.spiram.spi.writebytes(arr)
  if len(arr)!=720:    # The source buffer was not full. Did we run out of time?
    print ('x',len(arr),end='') # If you see this, we have failed
  # Done with this buffer 
  tail=(tail+1)%BUFFERS
  # Get ready to transmit. Do it now while we have plenty of time
  fifo.transmit()

print ('vbit.py System started')

try:
  # This thread will be used to read the input stream into a field buffer
  while True:

    #if bus.read_byte_data(0x20,0x10)&1 != 0:
    #  GPIO.output(18, GPIO.HIGH)
    #else:
    #  GPIO.output(18, GPIO.LOW)

    ###### Wait while the buffers are full ######
    while (head+1)%BUFFERS == tail:
      time.sleep(0.0005)
    ###### load the next buffer ######
    buf[head].clearBuffer()
    # load a field of 16 vbi lines
    for line in range(16):  
      # packet=file.read(packetSize) # file based version
      packet=sys.stdin.buffer.read(packetSize) # read binary from stdin
      buf[head].addPacket(packet)
    ##### step to the next buffer
    head=(head+1)%BUFFERS
    
    # Sequence the startup so we get fully buffered before we start transmitting
    if countdown==1: # now the buffer is full we can enable interrupts
      GPIO.add_event_detect(GPIO_FLD, GPIO.BOTH, callback=fieldEdge) # Look for the field pulse   
    if countdown>0:
      countdown-=1

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
  print("Keyboard interrupt")    

except:
  print("some error") 

finally:
  print("clean up") 
  GPIO.output(GPIO_LED, GPIO.LOW)
  #GPIO.output(24, GPIO.LOW)
  GPIO.cleanup() # cleanup all GPIO
