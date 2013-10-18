from django_socketio import events
from variables import variables as var
#from gps_navigation.Track import Point
from navigation.models import Route, Coord;

import xml.etree.ElementTree as ET
from xml.dom import minidom

inc = 3;

def to_bdd():
    point = Point('trackcompleto.xml','tr.xml')
    pp = point.get();
    print pp
    rout = Route.objects.create(name="TrackCompleto");
    pp == -1
    k=0;
    while pp != 0 or k>5:
        pp = point.get();
        print pp
        k+=1;
        cor = Coord.objects.create(route=rout,lat=float(pp[0]),lon=float(pp[1]),speed=float(pp[2]),track=float(pp[3]),time=pp[4]);
        #return [lat, lon,speed,time,track]

@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    print "hola"
    route = {};

    rout = Route.objects.get(id=4);
    coords = Route.get_only_coord(rout);

    if message.has_key('action'):
        print "get_route"
        route = {'action':'route','series': {"label": "Route0", "data":coords}}
    socket.send(route)



@events.on_message(channel="hand_control")
def message(request, socket, context, message):

    print "manual_control"

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
            pass
        to_brodcast = {'action':'coord_inLine','series': {"label": "inLine", "data":[[var.ad_value, var.ws_value]]}}
        to_channel = {'action':'update','ws': var.ws_value,'ad':var.ad_value};

        #socket.broadcast_channel({"action": "message", "message":"manual_control"}, 'logger')
        socket.broadcast_channel(to_brodcast, 'navigation')
        socket.send_and_broadcast_channel(to_channel)
    except:
        pass

class Point:
    "Optimizar la parte de abrir y cerrar el fichero"
    def __init__ (self, fichin, fichout):
        self.numelem = 0
        try:
            self.tree = ET.parse(fichin)
            self.root = self.tree.getroot()
        except:
            print "Ausencia de fichero de entrada"
        try:
            self.fichout=fichout
            fichero = open(self.fichout, "w+")
            implementacion_DOM = minidom.getDOMImplementation()
            self.xml_document = implementacion_DOM.createDocument(None, "data", None)
            self.xml_document.writexml(fichero, encoding='utf-8')
            fichero.close()
        except:
            print "Ausencia de fichero de salida"

    def get(self):
        """Devuelve la latitud y la longitud en una lista."""
        try:
            lat = self.root[self.numelem][0].text
            lon = self.root[self.numelem][2].text
            speed = self.root[self.numelem][1].text
            time = self.root[self.numelem][3].text
            track = self.root[self.numelem][4].text
            self.numelem += 1
            return [lat, lon,speed,time,track]
        except:
            return 0

    def put(self, datadic):
        """Recibe un diccionario y mete esos datos en un fichero xml"""
        try:
            raiz_documento = self.xml_document.documentElement
            #Creo nodo
            nodo = self.xml_document.createElement("coordenada")
            #Creo elemento
            for key in datadic.keys():
                elemento = self.xml_document.createElement(key)
                #innerXML, text
                elemento.appendChild(self.xml_document.createTextNode(str(datadic[key])))
                #Anido elemento en nodo
                nodo.appendChild(elemento)
                #Anido nodo en raiz
            raiz_documento.appendChild(nodo)
            fichero = open(self.fichout, "w")
            self.xml_document.writexml(fichero, encoding='utf-8')
            fichero.close()
            return 1
        except:
            return 0
