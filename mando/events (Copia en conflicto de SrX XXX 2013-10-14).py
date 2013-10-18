from django_socketio import events
import models



@events.on_message(channel="manual_control")
def message(request, socket, context, message):

    new_param={}
    if 'type' in message  and  message['type']=='manual_control':
        if message["actionx"] == "w":
            print "wwww"
            models.ws_value+=1
            new_param = {"action": "message", "actionx": "w", "value": models.ws_value }

        elif message["actionx"] == "s":
            models.ws_value-=1
            new_param = {"action": "message", "actionx": "s", "value": models.ws_value}

        elif message["actionx"] == "a":
            models.ad_value-=1
            new_param = {"action": "message", "actionx": "a", "value": models.ad_value}

        elif message["actionx"] == "d":
            models.ad_value+=1
            new_param = {"action": "message", "actionx": "d", "value": models.ad_value}

        elif message["actionx"] == "stop":
            new_param = {"action": "message", "actionx": "stop", "value": 90}
            models.ws_value = 90
            models.ad_value = 90
        else:
            print "its ok"
    else:
        print "no actionx"
    print str(models.ws_value) + " " + str(models.ad_value)
    socket.broadcast_channel({"action": "message", "message":"manual_control"}, 'logger')
    socket.broadcast_channel({"action": "coord", "message":"navigation","x":models.ws_value,"y":models.ad_value}, 'navigation')
    socket.send_and_broadcast_channel(new_param)
