from django.conf.urls import url
from django.contrib import admin
from teach import views


urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^emp/$', views.get_emp, name='emp'),
    url(r'^teachers/$', views.get_teachers, name='teachers'),
    url(r'^subjects/$', views.get_subjects, name='subjects'),
    url(r'^search/$', views.search, name='search'),
    url(r'^jsontest/$', views.jsontest),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'emp/(\d)/$', views.get_single_emp),
]
