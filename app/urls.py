from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    #path('', home, name="home"),
    path('', views.HomeView.as_view(template_name = 'index.html'), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('userhome/', views.userhome, name='userhome'),
    # path('userhome/', views.HomeView.as_view(template_name='userindex.html'), name='userhome'),
    path('instructions/', views.instructions, name='instructions'),
    path('about_us/', views.about_us, name='about_us'),
    path('my_subjects/', views.my_subjects, name='my_subjects'),
    path('user/profile/', views.profile, name='profile'),
]
