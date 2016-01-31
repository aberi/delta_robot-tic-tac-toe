import serial
import time

ser = serial.Serial('/dev/cu.usbmodemFD121', 9600)
time.sleep(1)
ser.write(chr(1))
