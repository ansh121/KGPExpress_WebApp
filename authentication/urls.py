from django.urls import path
from .views import login_view, register_user, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]
