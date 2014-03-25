import sys
import serial
import time
import threading
import logging #no se si hace falta
import car_control as CC
import gps_c
from navigation.coord import *
from navigation.models import Route, Coord
from django_socketio import broadcast_channel
from django_socketio import NoSocket

fgps = 0.2
intervalo_envio = 5 # Para sacar cada cuanto se envia la info: fgps * intervalo

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
            print "Guardando en base de datos nueva ruta.."
            route=[]
            while not self.stopped():
                i+=1
                time.sleep(fgps)
                cp = bth.gpsInfo
                if (i % int(self.interoute)) == 0 and float(cp['lon']) != 0.0:
                    route_point=[]
                    route_point=[float(cp['lat']), float(cp['lon']), float(cp['track']), float(cp['speed']), cp['time']]
                    route.append(route_point)
                    print "Punto guardado: " + str(cp['lat']) + " " + str(cp['lon'])
            rout = Route.objects.create(name=self.nameroute)
            for point in route:
                cor = Coord.objects.create(route=rout, lat=point[0], lon=point[1], track=point[2], speed=point[3], time=point[4]);
        except:
            raise

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class BroadcastThread(threading.Thread):
    def __init__(self):
        super(BroadcastThread, self).__init__()
        self.gpsInfo = {}

    def run(self):
        jj=0
        while True:
            jj+=1
            time.sleep(fgps);
            self.gpsInfo = _gps.update()
            try:
                if (jj % intervalo_envio) == 0:
                    broadcast_channel({'action':'gpsInfo', 'gpsData': self.gpsInfo}, 'navigation')
                    print "Info GPS"
            except NoSocket:
                print "No socket GPS"
                time.sleep(5);

class RouteThread(threading.Thread):

    def __init__(self, route_id):
        super(RouteThread, self).__init__()
        self.route_id = route_id
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    
    def run(self):
        route_id = self.route_id;
        print route_id
        time.sleep(1);
        
        try:
            broadcast_channel({'action':'startRoute -AA'}, 'navigation')
            time.sleep(1);
        except NoSocket:
            time.sleep(5);
        except:
            raise
        try:
            j=0
            rout = Route.objects.get(id=route_id)
            coords = Route.get_only_coord(rout)
            for point in coords:
                if self.stopped():
                    break
                try:
                    vehicle.speed(94)#velocidad minima
                    time.sleep(8)#tiempo que va a estar yendo en linea recta para inicializar
                except:
                    pass
                reached = False;
                infopoint={'action':'next_point', 'lon': point[0], 'lat': point[1]}
                broadcast_channel(infopoint, 'navigation')
                while not reached and not self.stopped():
                    j+=1
                    time.sleep(fgps);
                    gpsData = bth.gpsInfo
                    if str(gpsData['track']) != "nan":
                        dist = distance_to(point, gpsData)
                        H=heading_to(point, gpsData)
                        angle_diff = get_angle_diff(gpsData['track'], H)
                        turn_angle = angle_to_turn_angle(angle_diff) #lo devuelve como int
                        try:
                            vehicle.turn(turn_angle)
                        except:
                            pass
                        infopoint={'action':'state_route', 'lat': gpsData['lat'], 'lon': gpsData['lon'], 'dist': dist}
                        if (j % intervalo_envio) == 0:
                            broadcast_channel(infopoint, 'navigation')
                            print 'gpsData: ' + str(gpsData['lat']) + ' ' + str(gpsData['lon']) + ' Next point: ' + str(point) + ' Distance: ' +str(dist) + ' Turn angle: ' + str(turn_angle)
                        # socket.send({"action": "dox_route", "gpsData": gpsData,"nextPoin": point, 'distance_to': dist})
                        if dist < 300 and dist != -1:
                            reached = True
                            print '================ FIESTA =================== PUNTO ALCANZADO'
            print "Ruta terminada"
            del _thrd['RouteThread']
            broadcast_channel({'action':'routeIsStopped'}, 'navigation')
            vehicle.speed(90)
            vehicle.turn(90)
      
        except:
            raise

vehicle = CC.Control()

_thrd = dict()

_gps = gps_c.StartGps();

bth = BroadcastThread()
bth.setDaemon(True)
bth.start()