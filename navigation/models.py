from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=80)

    def get_only_coord(route_id):
        obj = Coord.objects.filter(route=route_id);
        #print obj
        coords = [];
        for o in obj:
            #print "--A"
            #print o.lat +' '+ o.lon
            coords.append([o.lat, o.lon])
        return  coords


class Coord(models.Model):
    route = models.ForeignKey(Route)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    track = models.FloatField(default=0.0)

    time = models.CharField(max_length=90)
