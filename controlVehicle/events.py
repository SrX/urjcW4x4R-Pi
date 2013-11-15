from django_socketio import events
from django_socketio import broadcast_channel

from controlVehicle import *
from controlVehicle import RecordThread
from navigation.models import Route, Coord;
from navigation import _gps;
from navigation import _thrd
import time
import threading

@events.on_message(channel="hand_control")
def message(request, socket, context, message):
    print "manual_control"
    try:
        if message['action'] == 'startroute':
            if not _thrd.has_key('RecordThread'):
                _thrd['RecordThread'] = RecordThread()
                _thrd['RecordThread'].setDaemon(True)
                _thrd['RecordThread'].start()
                rec.recording=1
                socket.send_and_broadcast_channel({'action':'startedroute'}) #tabular
        elif message['action'] == 'stoproute':
            _thrd['RecordThread'].stop()
            del _thrd['RecordThread']
            print "Nueva ruta guardada en base de datos"
            rec.recording=0
            socket.send_and_broadcast_channel({'action':'stoppedroute'})
        elif message['action'] == 'init':
            print str(vehicle.ws_value)
            print str(rec.recording)
            ret = {'action':'init', 'ws': vehicle.ws_value, 'ad': vehicle.ad_value, 'recording': rec.recording};
            socket.send_and_broadcast_channel(ret)
        else:
            ws_value, ad_value = vehicle.action(message['action'])
            ret = {'action':'update', 'ws': ws_value, 'ad':ad_value};
            socket.send_and_broadcast_channel(ret)
    except:
        raise