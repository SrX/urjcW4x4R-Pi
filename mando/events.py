from django_socketio import events
from django_socketio import broadcast_channel
from variables import variables as var
import django_socketio
from variables import _gps as _gps
from variables import vehicle as vehicle
from variables import ssoket as ssoket
from navigation.models import Route, Coord;
import sys


import gps

import time
# import xml.etree.ElementTree as ET
# from xml.dom import minidom

# from gps_navigation.gpsData import gpsData

inc = 3;
intervalo = 5;
nameroute = "Ruta 1 de cada 5"
# def to_bdd():
#     point = Point('trackcompleto.xml','tr.xml')
#     pp = point.get();
#     print pp
#     rout = Route.objects.create(name="TrackCompleto");
#     pp == -1
#     k=0;
#     while pp != 0 or k>5:
#         pp = point.get();
#         print pp
#         k+=1;
#         cor = Coord.objects.create(route=rout,lat=float(pp[0]),lon=float(pp[1]),speed=float(pp[2]),track=float(pp[3]),time=pp[4]);
#         #return [lat, lon,speed,time,track]


def from_gps_to_bdd(intervalo):
    try:
        # rout = Route.objects.create(name="Route " + str(var.nroute));
        rout = Route.objects.create(name=nameroute);
        print "Guardando en base de datos nueva ruta.."
        for i in range(1, 400):
            cp = _gps.update();
            if (i % intervalo) == 0 and float(cp['lon']) != 0.0:
                cor = Coord.objects.create(route=rout, lat=float(cp['lat']), lon=float(cp['lon']), track=float(cp['track']), speed=float(cp['speed']), time=cp['time']);
        # var.nroute+=1;
        print "Nueva ruta guardada en base de datos"
    except:
        print "Unexpected error: -z-", sys.exc_info()[0]

def do_route(rid):
    print 'do_route'
    rout = Route.objects.get(id=4);
    coords = Route.get_only_coord(rout);


# coords.append([o.lat, o.lon])
# def distance_to(point, to_point):

# def do_route(rid,socket):
#     socket.broadcast_channel({"action": "do_route", "started": 'yes'}, 'navigation')

#     print 'do_route'
#     rout = Route.objects.get(id=4);
#     coords = Route.get_only_coord(rout);

#     for point in coords:
        
#         reached = False;
#         while not reached:
#             gpsData = _gps.update()
#             dist = distance_to(gpsData, point)
#             print str(point) + str(dist)
#             socket.send_and_broadcast_channel({"action": "do_route", "gpsData": gpsData,"nextPoin": point,
#                                      'distance_to': dist})

#             if dist < 100:
#                 reached = True

#     socket.broadcast_channel({"action": "do_route", "finish": 'yes'}, 'navigation')

#     print "Ruta Terminada"
#     #print coords
#     pass



import thread
import time



# Define a function for the thread
def print_time(threadName, delay, socket):
   count = 0
   while count < 5:
    time.sleep(delay)
    count += 1
    route = {'action':threadName}
    socket.send(route)
    print "%s: %s" % (threadName, time.ctime(time.time()))

# Create two threads as follows



@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    print 'chan chan chan'
    try:
        if message['action'] == 'blublu':
            print 'entro en condicion'
            try:

               thread.start_new_thread(print_time, ("Thread-1", 2, socket))
               thread.start_new_thread(print_time, ("Thread-2", 4, socket))

            except:
                print "Unexpected error blublu:", sys.exc_info()[0]
            print 'saldo de condicion'

        elif message['action'] == 'do_route':

            try:
                socket.send({"action": "xdo_route", "started": 'yes'})
            except:
                print "Unexpected error do_route:", sys.exc_info()[0]


            try:
                rout = {}
                rout = Route.objects.get(name="Track95");
                coords = Route.get_only_coord(rout);
                coords = coords[1:10]
                for point in coords:
                    print 'do_route'
                    reached = False;
                    while not reached:
                        gpsData = _gps.update()
                        dist = distance_to(gpsData, point)

                        print str(point) + '   ' + str(dist)
                        
                        try:
                            route = {"action": "do_route", "gpsData": gpsData, "nextPoin": point, 'distance_to': dist}
                            socket.send(route)
                        except:
                            print "Unexpected error do_route:", sys.exc_info()[0]

                        # socket.send({"action": "dox_route", "gpsData": gpsData,"nextPoin": point, 'distance_to': dist})
                        print ' -z'

                        if dist < 100:
                            reached = True

                socket.send({"action": "xdo_route", "finish": 'yes'})
            except:
                print "Unexpected error do_route after:", sys.exc_info()[0]
            print 'do_route'
            print "Ruta Terminada"

        elif message['action'] == 'get_route':
            # print "get_route"
            route = {};
            rout = Route.objects.get(id=message['route_id']);
            coords = Route.get_only_coord(rout);
            route = {'action':'route', 'series': {"label": rout.name, "data":coords}}
            socket.send(route)

        elif message['action'] == 'get_routes':
            routes = Route.objects.all();
            print routes;
            routeslist = []
            for route in routes:
                routeinfo = []
                routeinfo.append(route.name)
                routeinfo.append(route.id)
                routeslist.append(routeinfo)
            print "AQUIIIIIIIII"
            route2 = {'action':'get_routes','info': routeslist}
            socket.send(route2)

        elif message['action'] == 'get_gps_data':
            try:
                gpsData = _gps.update()
                gpsInfo = {'action':'gpsInfo', 'gpsData': gpsData}
            except:
                print "Unexpected error get_gps_data ->:", sys.exc_info()[0]

                gpsInfo = {'action':'gpsInfo', 'gpsData': ''}


            socket.send(gpsInfo)

    except:
        print "Unexpected error: -z-", sys.exc_info()[0]

def evalue_wa(ws, ad):
    if ws > 120:
        ws = 120
    elif ws < 60:
        ws = 60
    
    if ad > 120:
        ad = 120
    elif ad < 60:
        ad = 60

    return ws, ad  

@events.on_message(channel="hand_control")
def message(request, socket, context, message):

    print "manual_control"
    # print var.gps.Update()
    print message
    print context

    try:
        if message['action'] == 'w':
            var.ws_value += inc
        elif message['action'] == 's':
            var.ws_value -= inc
        elif message['action'] == 'd':
<<<<<<< HEAD
            var.ad_value -= inc
        elif message['action'] == 'a':
            var.ad_value += inc
=======
            var.ad_value+=inc
        elif message['action'] == 'a':
            var.ad_value-=inc
>>>>>>> 64ff68e8b2559ede93be909a7b8696be3e952444
        elif message['action'] == 'q':
            var.ad_value = 90;
            var.ws_value = 90;
        elif message['action'] == 'startroute':
            from_gps_to_bdd(intervalo);

            
        var.ws_value, var.ad_value = evalue_wa(var.ws_value, var.ad_value)

        # to_brodcast = {'action':'coord_inLine','series': {"label": "inLine", "data":[[var.ad_value, var.ws_value]]}}
        to_channel = {'action':'update', 'ws': var.ws_value, 'ad':var.ad_value};

        # socket.broadcast_channel({"action": "message", "message":"manual_control"}, 'logger')
        # socket.broadcast_channel(to_brodcast, 'navigation')
        socket.send_and_broadcast_channel(to_channel)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass
    print 'out'


#################################

from math import *

# http://www.todopic.com.ar/foros/index.php?PHPSESSID=nvmismbs6oqmqvaf47euhib115&topic=26373.msg216172#msg216172
def distance_to(point, to_point):
    try:
        lat1 = radians(float(point['lat']))
        lon1 = radians(float(point['lon']))
        
        lat2 = radians(float(to_point[0]))
        lon2 = radians(float(to_point[1]))

        d = (acos(sin(lat1) * sin(lat2) \
              + cos(lat1) * cos(lat2) \
              * cos(lon1 - lon2)) * (6372797.560856 + 640) * 100)
        return d  # ESTA EN CM
    except:
        print "Unexpected error: distance_to: ", sys.exc_info()[0]
    
def heading_to(point, to_point):
    try:
        lat1 = radians(float(point[0]))
        lon1 = radians(float(point[1]))
        
        lat2 = radians(float(to_point['lat']))
        lon2 = radians(float(to_point['lon']))
        
        y = sin(lon2 - lon1) * cos(lat2)
        x = cos(lat1) * sin(lat2) \
          - sin(lat1) * cos(lat2) \
          * cos(lon2 - lon1)
        
        return (((degrees(atan2(y, x)) + 360 - 180) % 360))
    except:
        return -1

def get_angle_diff(track, heading_to):
    Total = float(heading_to) - (track)
    
    if Total > 180.0:
        Total = -(360 - Total)
    elif Total < -180.0:
        Total = 360 + Total
    return Total

def angle_to_turn_angle(angle):
    # ajustar angulo a partir del cual se hace maximo giro
    # valores negativos hacia la izquierda, valores < 90
    # valores positivos hacia la derecha, valores > 90
    if angle > 90:
        turn_angle = 120;
    elif angle < -90:
        turn_angle = 60;
    else:
        turn_angle = angle / 3 + 90
    return int(turn_angle)
