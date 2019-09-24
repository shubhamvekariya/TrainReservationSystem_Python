from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from main.models import admin_detail
from booking.models import  timetable_detail, train_detail, station_detail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
import math, random
# Create your views here

def admin_login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('admin_login.html', c)

def verification(request):
    admin = request.POST.get('username')
    password = request.POST.get('password')
    for i in admin_detail.objects.all():
        if admin == i.username and password == i.password:
            request.session['admin'] = admin
            return render(request, 'update.html')

    else:
        return render(request, 'admin_login.html', {'error': 'Enter a correct information'})


def admin_logout(request):
    del request.session['admin']
    return HttpResponseRedirect('/main/')


def add_train(request):
    name = request.POST.get('train_name')
    seat = request.POST.get('no_of_seat')
    add = train_detail(train_name=name , no_of_seat=seat)
    if add is not None:
        add.save()
        return render(request, 'update.html')
    else:
        return render(request, 'update.html', {'error': 'Does not work with empty'})


def delete_train(request):
    name = request.POST.get('train_name')
    d = train_detail.objects.get(train_name=name)
    if d is not None:
        d.delete()
        return render(request, 'update.html')
    else:
        return render(request, 'update.html', {'error': 'No Train For This Name'})



def add_station(request):
    name = request.POST.get('station_name')
    city = request.POST.get('city')
    add = station_detail(station_name=name, city=city)
    if add is not None:
        add.save()
        return render(request, 'update.html')
    else:
        return render(request, 'update.html', {'error': 'Does not work with empty'})

def delete_station(request):
    name = request.POST.get('station_name')
    d = train_detail.objects.get(station_name=name)
    if d is not None:
        d.delete()
        return render(request, 'update.html')
    else:
        return render(request, 'update.html', {'error': 'No Train For This Name'})

def addData(request):
    price = request.POST.get('price')
    distance = request.POST.get('distance')
    train_class = request.POST.get('train_class')
    aid = request.POST.get('arrival_station_id')
    did = request.POST.get('departure_station_id')
    no = request.POST.get('train_no')
    atime = request.POST.get('arrival_time')
    dtime = request.POST.get('departure_time')

    add = timetable_detail(arrival_time=atime, departure_time=dtime, price=price, distance=distance,
                           train_class=train_class, arrival_station_id_id=aid,  departure_station_id_id=did, train_no_id=no)
    if add is not None:
        add.save()
        return render(request, 'update.html')
    else:
        return render(request, 'update.html', {'error': 'Does not work with empty'})

def updateData(request):
    c = {}
    c.update(csrf(request))
    a = timetable_detail.objects.get(train_no_id=request.POST.get('train_no'))
    aid = request.POST.get('arrival_time')
    did = request.POST.get('departure_time')
    price = request.POST.get('price')
    distance = request.POST.get('distance')
    tc = request.POST.get('train_class')
    asi = request.POST.get('arrival_station_id')
    dsi = request.POST.get('departure_station_id')
    a.arrival_time = aid
    a.departure_time = did
    a.price = price
    a.distance = distance
    a.train_class = tc
    a.arrival_station_id_id = asi
    a.departure_station_id_id = dsi
    if a is not None:
        a.save()
        return render(request, 'update.html')
    else:
        return render(request, 'update.html', {'error': 'Does not work with empty'})
