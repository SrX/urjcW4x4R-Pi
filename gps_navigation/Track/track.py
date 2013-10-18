#!/usr/bin/python

import xml.etree.ElementTree as ET
from xml.dom import minidom

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
            self.numelem += 1
            return [lat, lon]
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
    
if __name__ == '__main__':
    x = Point('trackcompleto.xml', 'track.xml')
    y = x.get()
    print y
    y = x.get()
    print y
    y = x.get()
    print y
    x.put({"speed":"rapido","course":"0","utc":"now, but not that now","latlong":"somewhere","date":"now"})
    x.put({"speed":"muy rapido","course":"3","utc":"now","latlong":"there","date":"the future"})