from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from booking.models import station_detail,train_detail,timetable_detail, detail, train_seat_availability
from operator import itemgetter
from django.http import HttpResponseRedirect
from datetime import date, datetime

# Create your views here.
def pnrstatus(request):
    c = {}
    c.update(csrf(request))
    pnrno = request.POST.get('pnrno')
    a = detail.objects.get(pnr_no=pnrno)
    t = timetable_detail.objects.get(timetable_id=a.timetable_id)
    train_name = train_detail.objects.get(train_no=t.train_no_id).train_name
    data = []
    temp = {}
    b = station_detail.objects.get(station_id=t.arrival_station_id_id)
    c = station_detail.objects.get(station_id=t.departure_station_id_id)
    temp["acity"] = b.city
    temp["dcity"] = c.city
    temp["aname"] = b.station_name
    temp["dname"] = c.station_name
    temp["trainname"] = train_name
    temp["atime"] = t.arrival_time
    temp["dtime"] = t.departure_time
    temp["price"] = t.price * a.no_of_passenger
    temp["distance"] = t.distance
    temp["date"] = a.date
    temp["noofpassenger"] = a.no_of_passenger
    temp["train_class"] = t.train_class
    data.append(temp)
    return render(request, 'pnrstatus.html', {"detail": data})


def livestatus(request):
    c = {}
    c.update(csrf(request))
    pnrno = request.POST.get('pnrno')
    a = detail.objects.get(pnr_no=pnrno)
    train_no = timetable_detail.objects.get(timetable_id=a.timetable_id).train_no_id
    train_class = timetable_detail.objects.get(timetable_id=a.timetable_id).train_class
    train_name = train_detail.objects.get(train_no=train_no).train_name
    data1 = [{'trainno': train_no, 'trainname': train_name}]
    data = []
    for i in timetable_detail.objects.all():
        if i.train_no_id == train_no and i.train_class == train_class:
            temp = {}
            b = station_detail.objects.get(station_id=i.arrival_station_id_id)
            c = station_detail.objects.get(station_id=i.departure_station_id_id)
            temp["acity"] = b.city
            temp["dcity"] = c.city
            temp["aname"] = b.station_name
            temp["dname"] = c.station_name
            temp["atime"] = i.arrival_time
            temp["dtime"] = i.departure_time
            data.append(temp)
    data = sorted(data, key=itemgetter('atime'))
    data = sorted(data, key=itemgetter('dtime'))
    for i in range(len(data)):
        if i < len(data):
            for j in range(i):
                if data[i]['dtime'] == data[j]['dtime']:
                    del data[i]
    for i in range(len(data)):
        if i < len(data):
            for j in range(i):
                if data[i]['dtime'] == data[j]['dtime']:
                    del data[i]
    if a.date == date.today() and data[len(data)-1]['atime'] > datetime.now().time():
        for i in range(len(data)):
            if data[i]['dtime'] < datetime.now().time() and data[i]['atime'] > datetime.now().time():
                data2 = []
                temp = {}
                temp["acity"] = data[i]['acity']
                temp["dcity"] = data[i]['dcity']
                temp["aname"] = data[i]['aname']
                temp["dname"] = data[i]['dname']
                temp["atime"] = data[i]['atime']
                temp["dtime"] = data[i]['dtime']
                data2.append(temp)
        return render(request, 'livestatus.html', {"train_timetable": data2, "train_detail": data1})
    else:
        return HttpResponseRedirect('/home/')

def myorder(request):
    c = {}
    c.update(csrf(request))
    username = request.session["username"]
    data = []
    for i in detail.objects.all():
        if i.username_id == username:
            temp ={}
            a = timetable_detail.objects.get(timetable_id=i.timetable_id)
            train_name = train_detail.objects.get(train_no=a.train_no_id).train_name
            temp["pnrno"] = i.pnr_no
            temp["noofpassenger"] = i.no_of_passenger
            temp["date"] = i.date
            temp["trainname"] = train_name
            b = station_detail.objects.get(station_id=a.arrival_station_id_id)
            c = station_detail.objects.get(station_id=a.departure_station_id_id)
            temp["acity"] = b.city
            temp["dcity"] = c.city
            temp["aname"] = b.station_name
            temp["dname"] = c.station_name
            temp["atime"] = a.arrival_time
            temp["dtime"] = a.departure_time
            temp["price"] = a.price*i.no_of_passenger
            temp["train_class"] = a.train_class
            data.append(temp)
    data = sorted(data, key=itemgetter('trainname'))
    data = sorted(data, key=itemgetter('date'), reverse=True)
    return render(request, 'myorder.html', {"detail": data})
