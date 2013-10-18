from django_socketio import events
from variables import variables as var

@events.on_message(channel="manual_control")
def message(request, socket, context, message):

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
    socket.broadcast_channel({"action": "coord", "message":"navigation",
                            "x":var.ws_value,"y":var.ad_value,
                            'series': {"label": "inLine", "data":[[var.ad_value, var.ws_value]]}}, 'navigation')
    socket.send_and_broadcast_channel(new_param)
