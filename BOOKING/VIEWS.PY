from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from booking.models import station_detail,train_detail,timetable_detail, detail, train_seat_availability
from login.models import passenger_detail
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
import datetime
import random
from operator import itemgetter

# Create your views here.
def showtrain(request):
    c = {}
    c.update(csrf(request))
    dcity = request.POST.get('departcity')
    acity = request.POST.get('arrivedcity')
    date = request.POST.get('date')
    astation = station_detail.objects.get(city=acity)
    dstation = station_detail.objects.get(city=dcity)
    request.session['date'] = date
    request.session['acity'] = acity
    request.session['dcity'] = dcity
    if date >= str(datetime.datetime.now()):
        data = []
        for i in timetable_detail.objects.all():
            if i.departure_station_id_id == dstation.station_id and i.arrival_station_id_id == astation.station_id:
                temp = {}
                temp["trainclass"] = i.train_class
                temp["acity"] = acity
                temp["dcity"] = dcity
                temp["aname"] = astation.station_name
                temp["dname"] = dstation.station_name
                temp["aid"] = astation.station_id
                temp["did"] = dstation.station_id
                temp["trainno"] = i.train_no_id
                temp["trainname"] = train_detail.objects.get(train_no=i.train_no_id).train_name
                temp["atime"] = i.arrival_time
                temp["dtime"] = i.departure_time
                temp["price"] = i.price
                data.append(temp)
        data = sorted(data, key=itemgetter('atime'))
        data = sorted(data, key=itemgetter('dtime'))
        data = sorted(data, key=itemgetter('trainname'))
        return render(request, 'showtrain.html', {"avail_trains": data})
    else:
        return HttpResponseRedirect('/home/')

def sortdata(request):
    c = {}
    c.update(csrf(request))
    acity = request.session['acity']
    dcity = request.session['dcity']
    date = request.session['date']
    astation = station_detail.objects.get(city=acity)
    dstation = station_detail.objects.get(city=dcity)
    request.session['date'] = date
    if date >= str(datetime.datetime.now()):
        data = []
        for i in timetable_detail.objects.all():
            if i.departure_station_id_id == dstation.station_id and i.arrival_station_id_id == astation.station_id:
                temp = {}
                temp["trainclass"] = i.train_class
                temp["acity"] = acity
                temp["dcity"] = dcity
                temp["aname"] = astation.station_name
                temp["dname"] = dstation.station_name
                temp["aid"] = astation.station_id
                temp["did"] = dstation.station_id
                temp["trainno"] = i.train_no_id
                temp["trainname"] = train_detail.objects.get(train_no=i.train_no_id).train_name
                temp["atime"] = i.arrival_time
                temp["dtime"] = i.departure_time
                temp["price"] = i.price
                data.append(temp)
    nameselect = (request.POST.get('nameselect', ''))
    atimeselect = (request.POST.get('atimeselect', ''))
    dtimeselect = (request.POST.get('dtimeselect', ''))
    if dtimeselect == "dtimedescending":
        data = sorted(data, key=itemgetter('dtime'), reverse=True)
        request.session['dtimeselect'] = "dtimedescending"
        if 'nameselect' in request.session:
            del request.session['nameselect']
        return render(request, 'showtrain.html', {"avail_trains": data})
    else:
        data = sorted(data, key=itemgetter('dtime'))
        if 'dtimeselect' in request.session:
            del request.session['dtimeselect']
    if nameselect == "namedescending":
        data = sorted(data, key=itemgetter('trainname'), reverse=True)
        request.session['nameselect'] = "namedescending"
        return render(request, 'showtrain.html', {"avail_trains": data})
    else:
        data = sorted(data, key=itemgetter('trainname'))
        if 'nameselect' in request.session:
            del request.session['nameselect']
    return render(request, 'showtrain.html', {"avail_trains": data})


def booking(request):
    c = {}
    c.update(csrf(request))
    trainno = request.POST.get('trainno')
    aid = request.POST.get('aid')
    did = request.POST.get('did')
    train_class = request.POST.get('train_class')
    date = request.session["date"]
    tem = {}
    tem["trainno"] = trainno
    tem["aid"] = aid
    tem["did"] = did
    tem["train_class"] = train_class
    if 'username' in request.session:
        if 'book' in request.session:
            tem1 = request.session["book"]
            trainno = tem1["trainno"]
            aid = tem1["aid"]
            did = tem1["did"]
            train_class = tem1["train_class"]
            del request.session["book"]
        book = timetable_detail.objects.get(train_no_id=trainno, departure_station_id_id=did, arrival_station_id_id=aid,
                                            train_class=train_class)
        a = 2
        for i in train_seat_availability.objects.all():
            if str(i.date) == str(date) and i.timetable_id == book.timetable_id:
                a = 1
        if a == 2:
            q = train_seat_availability(timetable_id=book.timetable_id, seat_availability=100, date=date)
            q.save()
        data = []
        temp = {}
        temp["aid"] = book.arrival_station_id_id
        temp["did"] = book.departure_station_id_id
        temp["trainno"] = book.train_no_id
        temp["trainname"] = train_detail.objects.get(train_no=book.train_no_id).train_name
        temp["atime"] = book.arrival_time
        temp["dtime"] = book.departure_time
        temp["price"] = book.price
        temp["distance"] = book.distance
        temp["train_class"] = train_class
        data.append(temp)
        return render(request, 'booking.html', {"bookdata": data})
    else:
        request.session['book'] = tem
        return HttpResponseRedirect('/login/')

def payment(request):
    c = {}
    c.update(csrf(request))
    trainno = request.POST.get('trainno')
    aid = request.POST.get('aid')
    did = request.POST.get('did')
    noofpassenger = request.POST.get('passenger')
    train_class = request.POST['train_class']
    noofpassenger = int(noofpassenger)
    username = request.session['username']
    date = request.session['date']
    del request.session['date']
    del request.session['acity']
    del request.session['dcity']
    book = timetable_detail.objects.get(train_no_id=trainno, departure_station_id_id=did, arrival_station_id_id=aid,
                                        train_class=train_class)
    astation = station_detail.objects.get(station_id=aid)
    trainname = train_detail.objects.get(train_no=book.train_no_id).train_name
    dstation = station_detail.objects.get(station_id=did)
    data = []
    target = train_seat_availability.objects.get(timetable_id=book.timetable_id, date=date)
    if noofpassenger <= target.seat_availability:
        PNR = random.randrange(1000000000, 1100000000)
        temp = {}
        temp["acity"] = astation.city
        temp["dcity"] = dstation.city
        temp["trainno"] = book.train_no_id
        temp["trainname"] = trainname
        temp["atime"] = book.arrival_time
        temp["dtime"] = book.departure_time
        temp["price"] = book.price*noofpassenger
        temp["distance"] = book.distance
        temp["fullname"] = passenger_detail.objects.get(username=username).full_name
        temp["date"] = date
        temp["noofpassenger"] = noofpassenger
        temp["pnr"] = PNR
        temp["train_class"] = train_class
        data.append(temp)
        target.seat_availability = target.seat_availability - noofpassenger
        target.save()
        s = detail(pnr_no=PNR, username_id=username, timetable_id=book.timetable_id,
                   no_of_passenger=noofpassenger, date=date, seat_availability_id=target.seat_availability_id)
        s.save()
        subject = 'Confirmation Mail For Booking'
        message = 'Your booking details are below.'+'\n'+'\nPNR Number:'+str(PNR)+'\nTrain Name:'+trainname + \
                  '\nClass:'+train_class+'\nNo. of Passanger:'+str(noofpassenger)+'\nArrival City:'+astation.city + \
                  '\nDeparture City:'+dstation.city+'\nArrival Time:'+str(book.arrival_time) + \
                  '\nDeparture Time:'+str(book.departure_time) + \
                  '\nDate:'+str(date)+'\nPrice:'+str(book.price*noofpassenger)+'\nDistance:'+str(book.distance)+'KM'
        from_email = settings.EMAIL_HOST_USER
        to_list = [request.session['email']]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return render(request, 'payment.html', {'bookdata': data})
    else:
        return HttpResponseRedirect('/home/')

def cancelticket(request):
    c = {}
    c.update(csrf(request))
    pnr_no = request.POST.get('pnrno')
    noofpassenger = request.POST.get('noofpassenger')
    noofpassenger = int(noofpassenger)
    a = detail.objects.get(pnr_no=pnr_no)
    b = train_seat_availability.objects.get(seat_availability_id=a.seat_availability_id)
    if noofpassenger <= a.no_of_passenger:
        if noofpassenger == a.no_of_passenger:
            b.seat_availability += noofpassenger
            detail.objects.get(pnr_no=pnr_no).delete()
        else:
            b.seat_availability += noofpassenger
            a.no_of_passenger -= noofpassenger
            a.save()
        b.save()
    return HttpResponseRedirect('/home/')


