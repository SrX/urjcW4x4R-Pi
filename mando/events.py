from django_socketio import events
from variables import variables as var
#from gps_navigation.Track import Point
from navigation.models import Route, Coord;

import xml.etree.ElementTree as ET
from xml.dom import minidom
trakeado = False;

def to_bdd():
    point = Point('trackcompleto.xml','tr.xml')
    pp = point.get();
    print pp
    rout = Route.objects.create(name="TrackCompleto");

    pp == -1
    while pp != 0:
        pp = point.get();
        print pp
        cor = Coord.objects.create(route=rout,lat=float(pp[0]),lon=float(pp[1]),speed=float(pp[2]),track=float(pp[3]),time=pp[4]);
        #return [lat, lon,speed,time,track]

@events.on_message(channel="navigation")
def navigation(request, socket, context, message):
    print "hola"
    route = {};
    #to_bdd();
    if message.has_key('action'):
        print "get_route"
        coords =  [[72,52],[43,34],[23,45],[1,2],[99,97]]
        route = {'action':'route','series': {"label": "Route0", "data":coords}}
    socket.send(route)



@events.on_message(channel="manual_control")
def message(request, socket, context, message):

    print "manual_control"
    new_param={}
    if 'type' in message  and  message['type']=='manual_control':
        if message["actionx"] == "w":
            var.ws_value=var.ws_value+5
            if var.ws_value>120:
                var.ws_value=120
            #var.car.speed(var.ws_value)
            new_param = {"action": "message", "actionx": "w", "value": var.ws_value }

        elif message["actionx"] == "s":
            var.ws_value=var.ws_value-5
            if var.ws_value<60:
                var.ws_value=60
            #var.car.speed(var.ws_value)
            new_param = {"action": "message", "actionx": "s", "value": var.ws_value}

        elif message["actionx"] == "a":
            var.ad_value=var.ad_value-5
            if var.ad_value<60:
                var.ad_value=60
            #var.car.turn(var.ad_value)
            new_param = {"action": "message", "actionx": "a", "value": var.ad_value}

        elif message["actionx"] == "d":
            var.ad_value=var.ad_value+5
            if var.ad_value>120:
                var.ad_value=120
            #var.car.turn(var.ad_value)
            new_param = {"action": "message", "actionx": "d", "value": var.ad_value}

        elif message["actionx"] == "stop":
            new_param = {"action": "message", "actionx": "stop", "value": 90}
            var.ad_value=90
            var.ws_value=90
            #var.car.turn(var.ad_value)
            #var.car.speed(var.ws_value)
        else:
            print "its ok"
    else:
        print "no actionx"
    print str(var.ws_value) + " " + str(var.ad_value)
    socket.broadcast_channel({"action": "message", "message":"manual_control"}, 'logger')
    socket.broadcast_channel({"action": "route", "message":"navigation",
                            "x":var.ws_value,"y":var.ad_value,
                            'series': {"label": "inLine", "data":[[var.ad_value, var.ws_value]]}}, 'navigation')
    socket.send_and_broadcast_channel(new_param)

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
