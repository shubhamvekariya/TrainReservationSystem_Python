from django.shortcuts import render
from django.views.generic import TemplateView
from booking.models import station_detail
# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        data = []
        for i in station_detail.objects.all():
            temp = {}
            temp['stationname'] = i.city
            data.append(temp)
        return render(request, 'home.html', {'stationname': data})
