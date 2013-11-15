from django_socketio import events
from django_socketio import broadcast_channel

from controlVehicle import *
from navigation.models import Route, Coord;
from navigation import _gps;
import time
import threading

def from_gps_to_bdd():
    intervalo = 8;
    nameroute = "Ruta prueba"
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
        raise

@events.on_message(channel="hand_control")
def message(request, socket, context, message):
    print "manual_control"
    try:
        if message['action'] == 'startroute':
            print "EMPIEZO GRABADO"
            t = threading.Thread(target=from_gps_to_bdd)
            t.start()
        else:
            ws_value, ad_value = vehicle.action(message['action'])
            ret = {'action':'update', 'ws': ws_value, 'ad':ad_value};
            
            socket.send_and_broadcast_channel(ret)
    except:
        raise