from django.db import models

# Create your models here.
class admin_detail(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=14)