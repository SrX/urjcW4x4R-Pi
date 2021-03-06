from math import *
import sys

# http://www.todopic.com.ar/foros/index.php?PHPSESSID=nvmismbs6oqmqvaf47euhib115&topic=26373.msg216172#msg216172
def distance_to(point, to_point):
    """Atencion a latitud/longitud de los puntos"""
    try:
        lat1 = radians(float(point[1]))
        lon1 = radians(float(point[0]))
        
        lat2 = radians(float(to_point['lat']))
        lon2 = radians(float(to_point['lon']))

        d = (acos(sin(lat1) * sin(lat2) \
              + cos(lat1) * cos(lat2) \
              * cos(lon1 - lon2)) * (6372797.560856 + 640) * 100)
        return d  # ESTA EN CM
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return -1
    
    
def heading_to(point, to_point):
    """Atencion a latitud/longitud de los puntos"""
    try:
        lat1 = radians(float(point[1]))
        lon1 = radians(float(point[0]))
        
        lat2 = radians(float(to_point['lat']))
        lon2 = radians(float(to_point['lon']))
        
        y = sin(lon2 - lon1) * cos(lat2)
        x = cos(lat1) * sin(lat2) \
          - sin(lat1) * cos(lat2) \
          * cos(lon2 - lon1)
        
        return (((degrees(atan2(y, x)) + 360 - 180) % 360))
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return -1

def get_angle_diff(track, heading_to):
    Total = float(heading_to) - (track)
    
    if Total > 180.0:
        Total = -(360 - Total)
    elif Total < -180.0:
        Total = 360 + Total
    return Total

def angle_to_turn_angle(angle):
    # ajustar angulo a partir del cual se hace maximo giro
    # valores negativos hacia la izquierda, valores < 90
    # valores positivos hacia la derecha, valores > 90
    if angle > 90:
        turn_angle = 105;
    elif angle < -90:
        turn_angle = 75;
    else:
        turn_angle = angle / 6 + 90
    return int(turn_angle)