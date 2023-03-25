import spidev
import time, sys
import OPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)

GPIO.output(12, GPIO.LOW)
time.sleep(0.1)
GPIO.output(12, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(12, GPIO.LOW)

spi=spidev.SpiDev()
spi.open(1,0)
#spi.max_speed_hz=7800000
spi.max_speed_hz=122000

time.sleep(1)

print("Trying to write...")

spi.writebytes([0x03,0x00])

print("Trying to read...")

print(spi.readbytes(20))
