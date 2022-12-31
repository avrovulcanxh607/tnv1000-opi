#!/usr/bin/env python3

# Buffering test vbit-test-py
# ../vbit2/vbit2 2> /dev/null | ./vbit-test.py
# Copyright (c) 2018 Peter Kwan
# MIT License.

import sys
import numpy as np


def reverse(x): # reverse the bit order in a byte
  x = ((x & 0xF0) >> 4) | ((x & 0x0F) << 4)
  x = ((x & 0xCC) >> 2) | ((x & 0x33) << 2)
  x = ((x & 0xAA) >> 1) | ((x & 0x55) << 1)
  return x  

def reverseBuffer(buf): # bit reverse each byte in buf
  b=bytearray()
  for ch in buf:
    b.append(reverse(ch)) 
  return b

class Buffer:
  #clockFrame = bytearray(b'\x55\x55\x27') # clock run-in and framing code
  clockFrame = b'\xaa\xaa\xe4' # clock run-in and framing code (reversed?)
  print ('Buffer created')
  def __init__(self):
    self.field=np.ndarray(shape=(16,45), dtype=np.uint8)
    self.count = 0 # The packet count
  def addPacket(self,pkt):
    p=bytearray(Buffer.clockFrame)
    p.extend(reverseBuffer(pkt))
    self.field[self.count]=p   
    self.count+=1
  def clearBuffer(self):
    self.count = 0 # The packet count
  def printPacket(self):
    for i in range(16):
      print (bytes(self.field[i]).hex())
