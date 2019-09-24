from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logout/', views.admin_logout),
    url(r'^login/', views.admin_login),
    url(r'^verification/', views.verification),
    url(r'^$', views.admin_login),
    url(r'^add/', views.add_train),
    url(r'^delete/', views.delete_train),
    url(r'^addStation/', views.add_station),
    url(r'^deleteStation/', views.delete_station),
    url(r'^addData/', views.addData),
    url(r'^updateData/', views.updateData),
]