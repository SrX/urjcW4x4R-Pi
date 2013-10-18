from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=80)

    def get_only_coord(self, route_id):
        obj = Coord.objects.filter(route=route_id);
        return obj


class Coord(models.Model):
    route = models.ForeignKey(Route)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    track = models.FloatField(default=0.0)

    time = models.CharField(max_length=90)
