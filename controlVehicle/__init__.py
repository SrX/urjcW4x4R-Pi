import gps
import sys
import serial
import time
import threading
from navigation.models import Route, Coord;
from navigation import _gps;

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def name_used(s):
    try:
        Route.objects.get(name=s)
        return True
    except:
        return False


class Control(object):
    def __init__ (self):
        self.ws_value = 90
        self.ad_value = 90
        
        # Paso del incremento
        self.inc = 3;
        
        try:
            self.arduino_conect = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        except:  # except (StopIteration):
            print "Unexpected error: Control ", sys.exc_info()[0]
            self.arduino_conect = ''
            pass
        
        self.reset()
        
        
    def reset(self):
        self.ws_value = 90
        self.ad_value = 90
        self.set(self.ws_value, self.ad_value)
        
    def action(self, action):
        if action == 'w':
            self.ws_value += self.inc
        elif action == 's':
            self.ws_value -= self.inc
        elif action == 'd':
            self.ad_value += self.inc
        elif action == 'a':
            self.ad_value -= self.inc
        else:  # action == 'q':
            # por medidas de seguridad, si el coche se escapa 
            # y/o el piloto se pone nervioso
            self.reset()
        
        self.evalue_wa()
        self.set(self.ws_value, self.ad_value)
        
        #devolver el valor, el que se ha pasado al coche
        return self.ws_value, self.ad_value
            
    def set(self, speed, angle):
        

        print 'Vehicle: s-' + str(speed) + ' a-' + str(angle)
        
        if self.arduino_conect != '':
            self.speed(speed)
            self.turn(angle)
        
    def speed(self, velocidad):
            self.arduino_conect.write(chr(255))
            self.arduino_conect.write(chr(2))
            self.arduino_conect.write(chr(velocidad))


    def turn(self, grados):
            self.arduino_conect.write(chr(255)) 
            self.arduino_conect.write(chr(1))
            self.arduino_conect.write(chr(grados))
            
    def evalue_wa(self):
        if self.ws_value > 120:
            self.ws_value = 120
        elif self.ws_value < 60:
            self.ws_value = 60
        
        if self.ad_value > 120:
            self.ad_value = 120
        elif self.ad_value < 60:
            self.ad_value = 60

class RecordThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, nameroute, interoute):
        super(RecordThread, self).__init__()
        self._stop = threading.Event()
        self.nameroute = nameroute
        self.interoute = interoute

    def run(self):
        i=0;
        try:
            rout = Route.objects.create(name=self.nameroute)
            print "Guardando en base de datos nueva ruta.."
            while not self.stopped():
                i+=1
                cp = _gps.update();
                if (i % int(self.interoute)) == 0 and float(cp['lon']) != 0.0:
                    print "Punto guardado"
                    cor = Coord.objects.create(route=rout, lat=float(cp['lat']), lon=float(cp['lon']), track=float(cp['track']), speed=float(cp['speed']), time=cp['time']);
        except:
            raise

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class Rec(object):
    def __init__ (self):
        self.recording = 0

vehicle = Control()
rec = Rec()