from django_socketio import events
from django_socketio import broadcast_channel


from navigation.models import Route, Coord;

from navigation import _gps

import time

import threading

import sys



def do_route(rid):
    print 'do_route'
    rout = Route.objects.get(id=4);
    coords = Route.get_only_coord(rout);




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

                class Looping(object):
                
                    def __init__(self):
                     self.isRunning = True
                
                    def runForever(self):
                       while self.isRunning == True:
                           time.sleep(1)
                           print 'tururu'
                           "do stuff here"
                
                l = Looping()
                t = threading.Thread(target = l.runForever)
                t.start()
                time.sleep(4)
                l.isRunning = False
               
               #thread.start_new_thread(print_time, ("Thread-1", 2, socket))
                thread.start_new_thread(print_time, ("Thread-2", 4, socket))

            except:
                print "Unexpected error blublu:", sys.exc_info()[0]
                raise
            print 'saldo de condicion'

        elif message['action'] == 'do_route':

            try:
                socket.send({"action": "xdo_route", "started": 'yes'})
            except:
                print "Unexpected error do_route:", sys.exc_info()[0]
                raise


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
                raise
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


