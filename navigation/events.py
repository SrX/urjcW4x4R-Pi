from django_socketio import events
from django_socketio import broadcast_channel


from navigation.models import Route, Coord;

from navigation import _gps
from navigation import _thrd
from navigation import RouteThread

import time

import threading

import sys


def do_route(rid):
    print 'do_route'
    rout = Route.objects.get(id=4);
    coords = Route.get_only_coord(rout);
    

import time

@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    print 'chan chan chan'
    try:
        if message['action'] == 'startRoute':
            if not _thrd.has_key('RouteThread'):
                rid  = message['rid']
                _thrd['RouteThread'] = RouteThread(rid)
                _thrd['RouteThread'].setDaemon(True)
                _thrd['RouteThread'].start()
                broadcast_channel({'action':'routeIsStart'}, 'navigation')
                
        elif message['action'] == 'stopRoute':
                print _thrd
                _thrd['RouteThread'].stop()
                del _thrd['RouteThread']
                broadcast_channel({'action':'routeIsStop'}, 'navigation')
                
        elif message['action'] == 'get_route':
            # print "get_route"
            route = {};
            rout = Route.objects.get(id=message['route_id']);
            coords = Route.get_only_coord(rout);
            route = {'action':'loadRoute', 'route': coords}
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
            route2 = {'action':'get_routes', 'info': routeslist}
            socket.send(route2)
    except:
        raise
        
        
        
        
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


