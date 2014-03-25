import time
import threading
import sys
from django_socketio import events
from django_socketio import broadcast_channel
from variables import _thrd
from variables import _gps
from variables import bth
from variables import vehicle
from variables import *
from navigation.models import Route, Coord
    
@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    try:
        if message['action'] == 'startRoute':
            if not _thrd.has_key('RouteThread'):
                if message['rid'] != -1:
                    print "message:" + message['rid']
                    _thrd['RouteThread'] = RouteThread(message['rid'])
                    _thrd['RouteThread'].setDaemon(True)
                    _thrd['RouteThread'].start()
                    print "guardado en dic: " + _thrd['RouteThread'].route_id
                    rout = Route.objects.get(id=message['rid']);
                    coords = Route.get_only_coord(rout);
                    broadcast_channel({'action':'routeIsStarted', 'route': coords}, 'navigation')
                
        elif message['action'] == 'stopRoute':
                _thrd['RouteThread'].stop()
                broadcast_channel({'action':'routeIsStopped'}, 'navigation')
                
        elif message['action'] == 'get_route':
            if not _thrd.has_key('RouteThread'):
                rout = Route.objects.get(id=message['route_id']);
                coords = Route.get_only_coord(rout);
                route = {'action':'loadRoute', 'route': coords}
                #broadcast_channel(route, 'navigation')
                socket.send(route)

        elif message['action'] == 'delete_route':
            if not _thrd.has_key('RouteThread'):
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
            try:
                rout = Route.objects.get(id=_thrd['RouteThread'].route_id);
                coords = Route.get_only_coord(rout);
                started = 1
                print "ESTO HA IDO"
            except:
                started = 0
            print "ESTA STARTED?????  " + str(started)
            route2 = {'action':'init', 'info': routeslist, 'routestate': started, 'routecoords': coords}
            socket.send(route2)
    except:
        raise