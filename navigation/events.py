import time
import threading
import sys
from django_socketio import events
from django_socketio import broadcast_channel
from variables import _thrd
from variables import _gps
from variables import bth
from variables import rs
from variables import vehicle
from variables import rec
from variables import *
from navigation.models import Route, Coord;

def do_route(rid):
    print 'do_route'
    rout = Route.objects.get(id=4);
    coords = Route.get_only_coord(rout);
    
@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    print 'chan chan chan'
    try:
        if message['action'] == 'startRoute':
            if not _thrd.has_key('RouteThread'):
                if message['rid'] != -1:
                    print message['rid']
                    _thrd['RouteThread'] = RouteThread(message['rid'])
                    _thrd['RouteThread'].setDaemon(True)
                    _thrd['RouteThread'].start()
                    rs.started = 1
                    rs.id = message['rid']
                    broadcast_channel({'action':'routeIsStarted'}, 'navigation')
                
        elif message['action'] == 'stopRoute':
                _thrd['RouteThread'].stop()
                #del _thrd['RouteThread']
                #rs.started=0
                broadcast_channel({'action':'routeIsStopped'}, 'navigation')
                
        elif message['action'] == 'get_route':
            if rs.started == 0:
                # print "get_route"
                rout = Route.objects.get(id=message['route_id']);
                coords = Route.get_only_coord(rout);
                route = {'action':'loadRoute', 'route': coords}
                socket.send(route)

        elif message['action'] == 'delete_route':
            if rs.started == 0:
                rout = Route.objects.get(id=message['route_id'])
                rout.delete();
                route = {'action':'deleted_route', 'id': message['route_id']}
                broadcast_channel(route, 'navigation')

        elif message['action'] == 'init':
            routes = Route.objects.all();
            routeslist = []
            for route in routes:
                routeinfo = []
                routeinfo.append(route.name)
                routeinfo.append(route.id)
                routeslist.append(routeinfo)
            coords=[]
            if rs.started==1:
                rout = Route.objects.get(id=rs.id);
                coords = Route.get_only_coord(rout);    
            route2 = {'action':'init', 'info': routeslist, 'routestate': rs.started, 'routecoords': coords}
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


