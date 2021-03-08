from django.conf.urls import url
from django.urls import path

from . import views
from .views import login_view, register_user, home
from django.contrib.auth.views import LogoutView

app_name = 'authentication'
urlpatterns = [
    #path('', home, name="home"),
    path('', views.HomeView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
