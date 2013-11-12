import gps
import sys
import serial
import time

# try:
#     _gps.next()
# except: 
#     print "Unexpected error: _gps.next() ", sys.exc_info()[0]


# gpsData =  {'lat'   :   _gps.fix.latitude,
#             'lon'   :   _gps.fix.longitude,
#             'track' :   _gps.fix.track,
#             'speed' :   _gps.fix.speed,
#             'time'  :   _gps.fix.time }
# #print gpsData

class StartGps(object):
    
    def __init__(self):
        self.gpsData = {}

        try:
            self._gps = gps.gps(mode=gps.WATCH_ENABLE|gps.WATCH_JSON|gps.WATCH_NEWSTYLE)
        except: #except (StopIteration):
            print "Unexpected error:", sys.exc_info()[0]
            self._gps = {}
            pass

    
    def update(self):
        try:
            self._gps.next()
        except StopIteration:
            print "Unexpected error: StartGps: ", sys.exc_info()[0]
            pass                #Hay que decidir que hacer si se produce un error.

        return          {'lat' :   self._gps.fix.latitude,
                        'lon'   :   self._gps.fix.longitude,
                        'track' :   self._gps.fix.track,
                        'speed' :   self._gps.fix.speed,
                        'time'  :   self._gps.fix.time,         #le pasa algo raro
                        #'date'     :   self._gps.fix.date,
                        #'alt'  :   self._gps.fix.altitude,
                        }

class Control(object):

    # arreglar el fallo del log
    def __init__ (self):
        try:
            self.arduino_conect = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        except: #except (StopIteration):
            print "Unexpected error: Control ", sys.exc_info()[0]
            self.arduino_conect = ''
            pass
    
        self.speed(90)
        self.turn(90)

    def speed(self, velocidad):
        print 'vehicle: v ' + str(velocidad)
        if self.arduino_conect != '':
            self.arduino_conect.write(chr(255))
            self.arduino_conect.write(chr(2))
            self.arduino_conect.write(chr(velocidad))


    def turn(self, grados):
        print 'vehicle: g ' + str(grados)
        if self.arduino_conect != '':
            self.arduino_conect.write(chr(255)) 
            self.arduino_conect.write(chr(1))
            self.arduino_conect.write(chr(grados))




vehicle = Control();
_gps = StartGps();



ssoket = None