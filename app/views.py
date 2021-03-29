from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import SearchForm
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from authentication.models import CustomUser
from authentication.forms import ProfileForm
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm

import environ

env = environ.Env()

class HomeView(generic.ListView):
    model = Event
    #model_2 = Subject
    # template_name = 'index.html'

    # template_name = 'authentication/modified_calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        # form = post(self)
        cal = Calendar(d.year, d.month)
        form = SearchForm(self.request.GET or None)
        subList = []
        if form.is_valid():
            query_code, query_name = (x for x in form.cleaned_data['subject'].split('-'))
            query_code = query_code.strip()
            query_year = form.cleaned_data['year']
            query_sem = form.cleaned_data['semester']
            context['subject'] = form.cleaned_data['subject']

            try:
                subject = Subject.objects.get(subject_code=query_code, semester=query_sem, year=query_year)
                subList.append(subject)

            except Subject.DoesNotExist:
                subject = None
                print("Subject Entry does not exist")
        else:
            print(form.errors)

        # sub = Subject()
        # sub.year = 2020
        # sub.description = 'aa'
        # sub.subject_name = 'ENGINEERING LABORATORY'
        # sub.department = 'CS'
        # sub.semester = 'Autumn'
        # sub.subject_code = 'EN19003'
        # sub.subject_id = '2'
        # sub.syllabus = 'daa'
        # sub.teacher_name = 'V'
        # sub.save()

        html_cal = cal.formatmonth(withyear=True,subList=subList)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        # context['form'] = form
        #print(context)
        print(form)
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

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    c_user = CustomUser.objects.get(username='nilesh')
    sub = Subject.objects.get(year=2020)
    instance.user = c_user
    instance.subject = sub
    
    form = EventForm(request.POST or None, instance=instance)
    print(form.data)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('app:calendar'))
    return render(request, 'event.html', {'form': form})


def instructions(request):
    return render(request, 'instructions.html')

def about_us(request):
    return render(request, 'about_us.html')

@login_required
def my_subjects(request):
    return render(request, 'my_subjects.html')

@login_required
def userhome(request):
    return HomeView.as_view(template_name='userindex.html')(request)
    # return render(request, 'userindex.html')

@login_required
def profile(request):
    if "submit_account_information" in request.POST:
        data = dict(request.POST)
        initial_data = {'username' : request.user.username}
        for k,v in data.items():
            initial_data[k]=v[0]
        print(initial_data)

        user=CustomUser.objects.update_or_create(initial_data)
        user.save()
        
        # # user = CustomUser.objects.get(user)
        # profile_form = ProfileForm(initial_data)
        # # profile_form.cleaned_data['username'] = request.user.username
        # print(profile_form,profile_form.is_valid(),profile_form.errors)
        # # profile_form['roll_no']="hello"
        # # if profile_form.is_valid():
        # # print(profile_form)
        # profile_form.save()

        # print(profile_form, profile_form.is_valid()) 

    return render(request, 'accounts/profile.html')