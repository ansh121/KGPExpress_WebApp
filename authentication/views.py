from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from verify_email.email_handler import send_verification_email
from validate_email import validate_email

import environ
env = environ.Env()

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            # print(form)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # print(username, password)
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
                
            else:
                msg = 'Authentication Failed'
        else:
            msg = 'Invalid Credentials'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        try:
            invalid_user = User.objects.get(username=request.POST['username'])
            if invalid_user.is_active==False:
                invalid_user.delete()
        except:
            print('new user')
        finally:
            if form.is_valid():
                
                # form.save()
                # username = form.cleaned_data.get("username")
                # raw_password = form.cleaned_data.get("password1")
                # user = authenticate(username=username, password=raw_password)

                # msg = 'User created - please <a href="/login">login</a>.'
                # success = True

                # is_valid = validate_email(email_address=form.cleaned_data.get("email"), check_mx=True)
                # is_valid = validate_email(form.cleaned_data.get("email"), verify=True)
                is_valid=True
                if(is_valid==False):
                    msg="Email does not exist!"
                else:
                    inactive_user = send_verification_email(request, form)
                    # print(inactive_user)
                    if inactive_user:
                        msg = "verification sent"
                        success = True
                    else:
                        msg = "Unable to send verification mail!"

                # return redirect("/login/")

            else:
                # print(form.errors.items())
                for field, errors in form.errors.items():
                    for error in errors:
                        msg=error
                        break

                # msg = 'Form is not valid'
                form = SignUpForm()

    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
