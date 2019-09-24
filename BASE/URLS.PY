from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'help/', views.help),
    url(r'aboutus/', views.aboutus),
    url(r'contactus/', views.contactus),
    url(r'review/', views.review),
]