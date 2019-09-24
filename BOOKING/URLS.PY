from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'showtrain/', views.showtrain),
    url(r'booking/', views.booking),
    url(r'sortdata/', views.sortdata),
    url(r'payment/', views.payment),
    url(r'cancelticket/', views.cancelticket),
]