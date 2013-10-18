from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=80)

class Coord(models.Model):
    route = models.ForeignKey(Route)
    lat = models.DecimalField(max_digits=20, decimal_places=10)
    lon = models.DecimalField(max_digits=20, decimal_places=10)
    speed = models.DecimalField(max_digits=7, decimal_places=4);
    track = models.DecimalField(max_digits=10, decimal_places=5);
    time = models.CharField(max_length=80)
