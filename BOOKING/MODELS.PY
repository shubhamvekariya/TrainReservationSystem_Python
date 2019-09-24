from django.db import models
from login.models import passenger_detail

# Create your models here.
class station_detail(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=30)
    city = models.CharField(max_length=15)

class train_detail(models.Model):
    train_no = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=30)
    no_of_seat = models.IntegerField()

class timetable_detail(models.Model):
    timetable_id = models.AutoField(primary_key=True)
    train_no = models.ForeignKey(train_detail, on_delete=models.CASCADE)
    arrival_station_id = models.ForeignKey(station_detail, related_name='arrival_station_id', on_delete=models.CASCADE)
    departure_station_id = models.ForeignKey(station_detail, related_name='departure_station_id', on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    price = models.IntegerField()
    distance = models.IntegerField()
    train_class = models.CharField(max_length=30)

class train_seat_availability(models.Model):
    seat_availability_id = models.AutoField(primary_key=True)
    timetable = models.ForeignKey(timetable_detail, on_delete=models.CASCADE)
    seat_availability = models.IntegerField()
    date = models.DateField()

class detail(models.Model):
    pnr_no = models.IntegerField(primary_key=True)
    timetable = models.ForeignKey(timetable_detail, on_delete=models.CASCADE)
    no_of_passenger = models.IntegerField()
    date = models.DateField()
    seat_availability = models.ForeignKey(train_seat_availability, on_delete=models.CASCADE)
    username = models.ForeignKey(passenger_detail, on_delete=models.CASCADE)

