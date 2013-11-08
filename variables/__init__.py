import gps
import sys

try:
	_gps = gps.gps(mode=gps.WATCH_ENABLE|gps.WATCH_JSON|gps.WATCH_NEWSTYLE)
except: #except (StopIteration):
    print "Unexpected error:", sys.exc_info()[0]
    _gps = {}
    pass


# def resetGps():
#     try:
#         return gps.gps(mode=gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)
#     except: #except (StopIteration):
#         print "Unexpected error:", sys.exc_info()[0]
#         return {}
#         pass


import serial, time

class Control:

    # arreglar el fallo del log
    def __init__ (self):
        self.arduino_conect = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.speed(90)
        self.turn(90)

    def speed(self, velocidad):
        self.arduino_conect.write(chr(255))
        self.arduino_conect.write(chr(2))
        self.arduino_conect.write(chr(velocidad))


    def turn(self, grados):
        self.arduino_conect.write(chr(255)) 
        self.arduino_conect.write(chr(1))
        self.arduino_conect.write(chr(grados))

#no quiere sin /dev/ttyUSB0
#vehicle = Control();