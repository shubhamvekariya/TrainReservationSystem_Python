from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'pnrstatus/', views.pnrstatus),
    url(r'livestatus/', views.livestatus),
    url(r'myorder/', views.myorder),
]