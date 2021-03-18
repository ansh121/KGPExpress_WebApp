from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name='authentication'
urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path("logout/", LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
]