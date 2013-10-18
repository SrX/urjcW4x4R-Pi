# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect

def log(request, template="log.html"):
    context = {}
    return render(request, template, context)

