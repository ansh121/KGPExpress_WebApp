from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, SearchForm
from verify_email.email_handler import send_verification_email
from validate_email import validate_email

from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm

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
            if invalid_user.is_active == False:
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
                is_valid = True
                if (is_valid == False):
                    msg = "Email does not exist!"
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
                        msg = error
                        break

                # msg = 'Form is not valid'
                form = SignUpForm()

    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def home(request):
    # if request.method == "POST":
    form = SearchForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data.items())
        print(request.POST)
    return render(request, "index.html", {"form": form})


class HomeView(generic.ListView):
    model = Event
    template_name = 'index.html'

    # template_name = 'authentication/modified_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        form = SearchForm(self.request.POST or None)
        if form.is_valid():
            print(form.cleaned_data.items())
            print(self.request.POST)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['form'] = form
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('authentication:calendar'))
    return render(request, 'event.html', {'form': form})
