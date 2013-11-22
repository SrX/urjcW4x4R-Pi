import gps
import sys
import serial
import time
import threading
from navigation.models import Route, Coord
from navigation import _gps

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

rec = Rec()