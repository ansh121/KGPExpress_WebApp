from django.urls import path
from . import views
from django.contrib.auth.views import *
from .forms import *
app_name='authentication'
urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path("logout/", LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path("password_reset/", PasswordResetView.as_view(template_name='accounts/password_reset.html', subject_template_name='accounts/subject.txt', html_email_template_name='accounts/password_reset_confirm_email.html'), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',form_class=ForgetPasswordForm), name='password_reset_confirm'),
    path("reset/done/", PasswordResetCompleteView.as_view(template_name='accounts/reset_done.html'), name="reset_done"),
]