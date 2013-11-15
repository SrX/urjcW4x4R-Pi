import threading

import logging
import time



_thrd = dict()



import sys
import gps

class StartGps(object):
    def __init__(self):
        self.gpsData = {}
        try:
            self._gps = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_JSON | gps.WATCH_NEWSTYLE)
        except:  # except (StopIteration):
            print "Unexpected error:", sys.exc_info()[0]
            self._gps = {}
            pass


    def update(self):
        try:
            self._gps.next()
        except StopIteration:
            print "Unexpected error: StartGps: ", sys.exc_info()[0]
            pass    
        except AttributeError:  # Hay que decidir que hacer si se produce un error.
            return      {'lat' :   0,
                        'lon'   :   0,
                        'track' :   0,
                        'speed' :   0,
                        'time'  :   0,  # le pasa algo raro
                        # 'date'     :   self._gps.fix.date,
                        # 'alt'  :   self._gps.fix.altitude,
                        }

        return  {'lat' :   self._gps.fix.latitude,
                'lon'   :   self._gps.fix.longitude,
                'track' :   self._gps.fix.track,
                'speed' :   self._gps.fix.speed,
                'time'  :   self._gps.fix.time,  # le pasa algo raro
                # 'date'     :   self._gps.fix.date,
                # 'alt'  :   self._gps.fix.altitude,
                }


_gps = StartGps();



from django_socketio import broadcast_channel
from django_socketio import NoSocket



class BrodcastThread(threading.Thread):
    def run(self):
        time.sleep(5);
        while True:
            time.sleep(1);
            gpsInfo = _gps.update()
            try:
                broadcast_channel({'action':'gpsInfo', 'gpsData': gpsInfo}, 'navigation')
            except NoSocket:
                time.sleep(5);
            


bth = BrodcastThread()
bth.setDaemon(True)
bth.start()
