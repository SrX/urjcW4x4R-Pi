# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect



def navigation(request, template="navigation.html"):

    context = {}
    return render(request, template, context)
# Create your views here.
