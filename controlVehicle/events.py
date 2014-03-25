import time
import threading
from django_socketio import events
from django_socketio import broadcast_channel
from variables import _thrd
from variables import _gps
from variables import bth
from variables import vehicle
from variables import *
from navigation.models import Route, Coord;

@events.on_message(channel="hand_control")
def message(request, socket, context, message):
    print "manual_control"
    try:
        if message['action'] == 'startroute':
            if is_integer(message['interv']) and not name_used(message['name']):
                if not _thrd.has_key('RecordThread'):
                    _thrd['RecordThread'] = RecordThread(message['name'], message['interv'])
                    _thrd['RecordThread'].setDaemon(True)
                    _thrd['RecordThread'].start()
                    socket.send_and_broadcast_channel({'action':'startedroute'}) #tabular
        elif message['action'] == 'stoproute':
            _thrd['RecordThread'].stop()
            del _thrd['RecordThread']
            print "Nueva ruta guardada en base de datos"
            socket.send_and_broadcast_channel({'action':'stoppedroute'})
        elif message['action'] == 'init':
            if not _thrd.has_key('RecordThread'):
                recording = 0
            else:
                recording = 1
            ret = {'action':'init', 'ws': vehicle.ws_value, 'ad': vehicle.ad_value, 'recording': recording};
            socket.send_and_broadcast_channel(ret)
        else:
            ws_value, ad_value = vehicle.action(message['action'])
            ret = {'action':'update', 'ws': ws_value, 'ad':ad_value};
            socket.send_and_broadcast_channel(ret)
    except:
        raise