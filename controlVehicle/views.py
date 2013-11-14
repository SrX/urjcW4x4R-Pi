# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect


def controlVehicle(request, template="controlVehicle.html"):
    context = {}
    return render(request, template, context)

