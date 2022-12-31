#!/usr/bin/env python

import smbus, time

#define SLAVE_ADDRESS_7113    (0x4a >> 1)
#define SLAVE_ADDRESS_7121    (0x88 >> 1)
# Set up the registers of a tnv1000 video DAC for teletext
#

decoder_registers = {
        0x0f:0x00,      # Power Up
        0x52:0xcd,      # SE_CVBS AFE IBIAS (not sure what this does)
        0x00:0x00,      # Set input to Ain1
        0x0e:0x80,      # "required write", apparently
        0x9c:0x00,      # Reset Current Clamp Circuitry [step1]
        0x9c:0xff,      # Reset Current Clamp Circuitry [step2]
        0x0e:0x00,      # Enter User Sub Map
        0x0e:0x80,      # Fast Switch
        0xd9:0x44,      # Fast Switch
        0x0e:0x40,      # Sub map 2
        0xe0:0x01,      # Enable fast switch
        0x0e:0x00,      # Normal map
        0x01:0x80,      # Video Selection 1: set to defaults
        0x02:0x85,      # Video Selection 2: PAL B/G/H/I/D
        0x03:0x8c,      # Output Control: Enable outputs, only filter active video
        0x04:0xb1,      # Extended Output Control: Enable colour in VBI
        0x07:0x01,      # Autodetect Enable: AD_PAL_EN (normal PAL Only)
        0x08:0x80,      # Contrast: default
        0x0a:0x00,      # Brightness: Default
        0x0b:0x00,      # Hue: Default
        0x0c:0x36,      # Free Run: Default
        0x0d:0x7c,      # Free Run: Default Cr Cb values
        0x13:0x00,
        0x14:0x01,      # Analog Clamp Control: Colour bars on free run
        0x15:0x00,      # Digital Clamp Control: Defaults
        0x17:0x41,      # Shaping Control Filter: Autoselection 2.17MHz # was 21
        0x18:0x93,      # Shaping Control Filter: Default
        0x19:0x03,      # Comb Filter Control: Widest bandwidth
        0x1d:0x40,      # ADI Control 2: Enable LLC
        0x27:0x32,      # Add max luma-chroma delay
        0x31:0x02,      # VS/FIELD Control
        0x51:0xe7,      # Lock Count
        0xf4:0x00,      # Low drive strength
        0xf9:0x04
}

def tnv1000():
  bus=smbus.SMBus(0)
  # 2a is the encoder
  bus.write_byte_data(0x2a, 0x00, 0x12)
  bus.write_byte_data(0x2a, 0x80, 0x11)
  bus.write_byte_data(0x2a, 0x82, 0xeb)
  bus.write_byte_data(0x2a, 0x83, 0x10)
  bus.write_byte_data(0x2a, 0x84, 0x00)
  bus.write_byte_data(0x2a, 0x8c, 0xcb)
  bus.write_byte_data(0x2a, 0x8d, 0x8a)
  bus.write_byte_data(0x2a, 0x8e, 0x09)
  bus.write_byte_data(0x2a, 0x8f, 0x2a)
  bus.write_byte_data(0x2a, 0xc9, 0x03)
  bus.write_byte_data(0x2a, 0xcb, 0xff)
  bus.write_byte_data(0x2a, 0xcc, 0xff)
  bus.write_byte_data(0x2a, 0xcd, 0xff)
  bus.write_byte_data(0x2a, 0xce, 0xff)

  try:
    bus.write_byte_data(0x20, 0x0f, 0x80)
  except:
    print("ignore bus error")

  time.sleep(5)
  for address, byte in decoder_registers.items():
    bus.write_byte_data(0x20, address, byte)

  #bus.write_byte_data(0x20, 0x00, 0x00)
  #bus.write_byte_data(0x20, 0x03, 0x8c)
  #bus.write_byte_data(0x20, 0x0f, 0x00)
  #bus.write_byte_data(0x20, 0x14, 0x01)
  #bus.write_byte_data(0x20, 0x1d, 0x40)

tnv1000()
