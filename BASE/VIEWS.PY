from django.shortcuts import render
from django.template.context_processors import csrf
# Create your views here.

def contactus(request):
    c = {}
    c = c.update(csrf(request))
    return render(request, 'contactus.html', c)
def help(request):
    c = {}
    c = c.update(csrf(request))
    return render(request, 'help.html', c)
def aboutus(request):
    c = {}
    c = c.update(csrf(request))
    return render(request, 'aboutus.html', c)
def review(request):
    c = {}
    c = c.update(csrf(request))
    return render(request, 'review.html', c)
