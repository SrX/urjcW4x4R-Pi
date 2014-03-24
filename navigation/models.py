from django.db import models

class Route(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    name = models.CharField(max_length=80)

    def get_only_coord(route_id):
        obj = Coord.objects.filter(route=route_id);
        #print obj
        coords = [];
        for o in obj:
            #print "--A"
            #print o.lat +' '+ o.lon
            coords.append([o.lon, o.lat])
        return  coords


class Coord(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.route
    route = models.ForeignKey(Route)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    track = models.FloatField(default=0.0)

    time = models.CharField(max_length=90)
