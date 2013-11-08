from django_socketio import events
from variables import variables as var

from variables import _gps as _gps
from variables import vehicle as vehicle

from navigation.models import Route, Coord;
import sys


import gps

import time
# import xml.etree.ElementTree as ET
# from xml.dom import minidom

# from gps_navigation.gpsData import gpsData

inc = 3;
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

<<<<<<< HEAD
=======
def from_gps_to_bdd():
    try:
        rout = Route.objects.create(name="Track95");
        for i in range(1, 300): 
            cp=_gps.update();
            if (i % 5) == 0 and float(cp['lon'])!=0.0:
                cor = Coord.objects.create(route=rout, lat=float(cp['lat']), lon=float(cp['lon']), track=float(cp['track']), speed=float(cp['speed']), time=cp['time']);
                print "Punto nuevo"
    except:
        print "Unexpected error: -z-", sys.exc_info()[0]

def do_route(rid):
    print 'do_route'
    rout = Route.objects.get(id=4);
    coords = Route.get_only_coord(rout);
>>>>>>> 8a96186b7e92e606a42eb32eeef9de03cbfbcf1d

#coords.append([o.lat, o.lon])
#def distance_to(point, to_point):

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

@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    print 'chan chan chan'
    try:
        if message['action'] == 'do_route':

            try:
                socket.send({"action": "xdo_route", "started": 'yes'})
            except:
                print "Unexpected error do_route:", sys.exc_info()[0]


            try:
                rout = {}
                rout = Route.objects.get(id=4);
                coords = Route.get_only_coord(rout);
                coords = coords[1:10]
                for point in coords:
                    print 'do_route'
                    reached = False;
                    while not reached:
                        gpsData = _gps.update()
                        dist = distance_to(gpsData, point)
                        #time.sleep(0.05)

                        print str(point) +'   '+ str(dist)
                        
                        try:
                            route = {"action": "do_route", "gpsData": gpsData,"nextPoin": point, 'distance_to': dist}
                            socket.send(route)
                        except:
                            print "Unexpected error do_route:", sys.exc_info()[0]

                        #socket.send({"action": "dox_route", "gpsData": gpsData,"nextPoin": point, 'distance_to': dist})
                        print ' -z'

                        if dist < 100:
                            reached = True

                socket.send({"action": "xdo_route", "finish": 'yes'})
            except:
                print "Unexpected error do_route after:", sys.exc_info()[0]
            print 'do_route'
            print "Ruta Terminada"

        elif message['action'] == 'get_route':
            #print "get_route"
            route = {};
            rout = Route.objects.get(name="Track95");
            coords = Route.get_only_coord(rout);
            route = {'action':'route','series': {"label": "Route0", "data":coords}}
            socket.send(route)

        elif message['action'] == 'get_routes':
            print "BUENAAAAAAAAAAAAAAAAAAAAAAAS"
            routes = Route.objects.all();
            print "HOLAAAAAAAAAAAA"
            print routes;
            #route = {'action':'route','series': {"label": "Route0", "data":coords}}
            #socket.send(route)

        elif message['action'] == 'get_gps_data':
            try:
                gpsData = _gps.update()
                gpsInfo = {'action':'gpsInfo','gpsData': gpsData}
            except:
                print "Unexpected error ->:", sys.exc_info()[0]

                gpsInfo = {'action':'gpsInfo','gpsData': ''}


            socket.send(gpsInfo)

    except:
        print "Unexpected error: -z-", sys.exc_info()[0]

def evalue_wa(ws,ad):
    if ws > 120:
        ws =120
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
    #print var.gps.Update()
    print message
    print context

    try:
        if message['action']=='w':
            var.ws_value+=inc
        elif message['action'] == 's':
            var.ws_value-=inc
        elif message['action'] == 'd':
            var.ad_value-=inc
        elif message['action'] == 'a':
            var.ad_value+=inc
        elif message['action'] == 'q':
            var.ad_value = 90;
            var.ws_value = 90;
        elif message['action'] == 'startroute':
            from_gps_to_bdd();

            
        var.ws_value, var.ad_value = evalue_wa(var.ws_value, var.ad_value)

        #to_brodcast = {'action':'coord_inLine','series': {"label": "inLine", "data":[[var.ad_value, var.ws_value]]}}
        to_channel = {'action':'update','ws': var.ws_value,'ad':var.ad_value};

        #socket.broadcast_channel({"action": "message", "message":"manual_control"}, 'logger')
        #socket.broadcast_channel(to_brodcast, 'navigation')
        socket.send_and_broadcast_channel(to_channel)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass
    print 'out'


#################################

from math import *

#http://www.todopic.com.ar/foros/index.php?PHPSESSID=nvmismbs6oqmqvaf47euhib115&topic=26373.msg216172#msg216172
def distance_to(point, to_point):
    try:
        lat1 = radians(float(point['lat']))
        lon1 = radians(float(point['lon']))
        
        lat2 = radians(float(to_point[0]))
        lon2 = radians(float(to_point[1]))

        d = (acos(sin(lat1) * sin(lat2) \
              + cos(lat1) * cos(lat2) \
              * cos(lon1 - lon2)) * (6372797.560856 + 640)*100 )
        return d # ESTA EN CM
    except:
        print "Unexpected error: distance_to: ", sys.exc_info()[0]
    
def heading_to(point, to_point):
    try:
        lat1 = radians(float(point[0]))
        lon1 = radians(float(point[1]))
        
        lat2 = radians(float(to_point['lat']))
        lon2 = radians(float(to_point['lon']))
        
        y = sin(lon2-lon1) * cos(lat2)
        x = cos(lat1) * sin(lat2) \
          - sin(lat1) * cos(lat2) \
          * cos(lon2-lon1)
        
        return (((degrees(atan2(y, x))+360-180) % 360))
    except:
        return -1

def get_angle_diff(track, heading_to):
    Total = float(heading_to) - (track)
    
    if Total > 180.0:
        Total = - (360 - Total)
    elif Total < -180.0:
        Total = 360 + Total
    return Total

def angle_to_turn_angle(angle):
    #ajustar angulo a partir del cual se hace maximo giro
    #valores negativos hacia la izquierda, valores < 90
    #valores positivos hacia la derecha, valores > 90
    if angle>90:
        turn_angle=120;
    elif angle<-90:
        turn_angle=60;
    else:
        turn_angle=angle/3+90
    return int(turn_angle)



# #################################################################################################
# class Point:
#     "Optimizar la parte de abrir y cerrar el fichero"
#     def __init__ (self, fichin, fichout):
#         self.numelem = 0
#         try:
#             self.tree = ET.parse(fichin)
#             self.root = self.tree.getroot()
#         except:
#             print "Ausencia de fichero de entrada"
#         try:
#             self.fichout=fichout
#             fichero = open(self.fichout, "w+")
#             implementacion_DOM = minidom.getDOMImplementation()
#             self.xml_document = implementacion_DOM.createDocument(None, "data", None)
#             self.xml_document.writexml(fichero, encoding='utf-8')
#             fichero.close()
#         except:
#             print "Ausencia de fichero de salida"

#     def get(self):
#         """Devuelve la latitud y la longitud en una lista."""
#         try:
#             lat = self.root[self.numelem][0].text
#             lon = self.root[self.numelem][2].text
#             speed = self.root[self.numelem][1].text
#             time = self.root[self.numelem][3].text
#             track = self.root[self.numelem][4].text
#             self.numelem += 1
#             return [lat, lon,speed,time,track]
#         except:
#             return 0

#     def put(self, datadic):
#         """Recibe un diccionario y mete esos datos en un fichero xml"""
#         try:
#             raiz_documento = self.xml_document.documentElement
#             #Creo nodo
#             nodo = self.xml_document.createElement("coordenada")
#             #Creo elemento
#             for key in datadic.keys():
#                 elemento = self.xml_document.createElement(key)
#                 #innerXML, text
#                 elemento.appendChild(self.xml_document.createTextNode(str(datadic[key])))
#                 #Anido elemento en nodo
#                 nodo.appendChild(elemento)
#                 #Anido nodo en raiz
#             raiz_documento.appendChild(nodo)
#             fichero = open(self.fichout, "w")
#             self.xml_document.writexml(fichero, encoding='utf-8')
#             fichero.close()
#             return 1
#         except:
#             return 0
