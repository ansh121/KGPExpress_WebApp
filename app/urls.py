from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    #path('', home, name="home"),
    path('', views.index, name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    url(r'^event/view/(?P<event_id>\d+)/$', views.event_view, name='event_view'),
    url(r'^event/delete/(?P<event_id>\d+)/$', views.event_delete, name='event_delete'),
    url(r'^userhome/(?P<subject_id>\d+)/$', views.subject_view, name='subject_view'),
    path('userhome/', views.userhome, name='userhome'),
    # path('userhome/', views.HomeView.as_view(template_name='userindex.html'), name='userhome'),
    path('instructions/', views.instructions, name='instructions'),
    path('about_us/', views.about_us, name='about_us'),
    path('my_subjects/', views.my_subjects, name='my_subjects'),
    path('user/profile/', views.profile, name='profile'),
    path('my_subjects/add_registered_subject/', views.add_registered_subject, name='add_registered_subject'),
    path('my_subjects/delete_registered_subject/', views.delete_registered_subject, name='delete_registered_subject'),
]
