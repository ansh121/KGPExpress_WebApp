from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    #path('', home, name="home"),
    path('', views.HomeView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('userhome/', views.userhome, name='userhome'),
    path('instructions/', views.instructions, name='instructions'),
    path('about_us/', views.about_us, name='about_us'),
    path('my_subjects/', views.my_subjects, name='my_subjects'),
]
