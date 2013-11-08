from django_socketio import events
from variables import variables as var

from variables import _gps as _gps
from variables import vehicle as vehicle

from navigation.models import Route, Coord;
import sys


import gps


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

def do_route(rid):
    print 'do_route'
    rout = Route.objects.get(id=4);
    coords = Route.get_only_coord(rout);

    for point in coords:
        gpsPoint = 12
    #print coords
    pass

@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    print 'chan chan chan'
    try:
        if message['action'] == 'do_route':
            do_route(message['route_id']);

        elif message['action'] == 'get_route':
            #print "get_route"
            route = {};
            rout = Route.objects.get(id=4);
            coords = Route.get_only_coord(rout);
            route = {'action':'route','series': {"label": "Route0", "data":coords}}
            socket.send(route)

        elif message['action'] == 'get_gps_data':
            try:
                # #print _gps

                # try:
                #     _gps.next()
                # except: 
                #     print "Unexpected error: _gps.next() ", sys.exc_info()[0]
                

                # gpsData =  {'lat'   :   _gps.fix.latitude,
                #             'lon'   :   _gps.fix.longitude,
                #             'track' :   _gps.fix.track,
                #             'speed' :   _gps.fix.speed,
                #             'time'  :   _gps.fix.time }
                # #print gpsData
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
