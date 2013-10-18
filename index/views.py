# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect

def to_index(request):
	return redirect("/index")
def index(request, template="index.html"):
    context = {}
    return render(request, template, context)
