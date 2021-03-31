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
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm

import environ
import json

env = environ.Env()


class HomeView(generic.ListView):
    model = Event

    # model_2 = Subject
    # template_name = 'index.html'

    # template_name = 'authentication/modified_calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        # form = post(self)
        # cal = Calendar(d.year, d.month)
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
        # sub.ltp ='2-0-1'
        # sub.credit = '4'
        # sub.save()
        eventList = []
        events = Event.objects.filter(subject__in=subList)
        # html_cal = cal.formatmonth(withyear=True,subList=subList)
        # context['calendar'] = mark_safe(html_cal)
        # context['prev_month'] = prev_month(d)
        # context['next_month'] = next_month(d)
        # context['event'] = "[{  \"title\": \"All Day Event\",  \"start\": new Date(y, m, 1)},{  \"id\": 999,  \"title\": \"Repeating Event\",  \"start\": new Date(y, m, d-3, 16, 0),  \"allDay\": false,  \"className\": \"info\"},{  \"id\": 999,  \"title\": \"Repeating Event\",  \"start\": new Date(y, m, d+4, 16, 0),  \"allDay\": false,  \"className\": \"info\"},{  \"title\": \"Meeting\",  \"start\": new Date(y, m, d, 10, 30),  \"allDay\": false,  \"className\": \"important\"},{  \"title\": \"Lunch\",  \"start\": new Date(y, m, d, 12, 0),  \"end\": new Date(y, m, d, 14, 0),  \"allDay\": false,  \"className\": \"important\"},{  \"title\": \"Birthday Party\",  \"start\": new Date(y, m, d+1, 19, 0),  \"end\": new Date(y, m, d+1, 22, 30),  \"allDay\": \"false\"},{  \"title\": \"Click for Google\",  \"start\": new Date(y, m, 28),  \"end\": new Date(y, m, 29),  \"url\": \"http://google.com/\",  \"className\": \"success\"},]"
        # eventStr = json.dumps(eventList)
        context['event'] = get_event_str(events)
        context['form'] = form
        print(context['event'])
        # print(form)
        return context


def get_event_str(events):
    eventStr = "["
    for ev in events:
        eventStr += "{  "
        eventStr += "\"title\": \"{event_name}\",  ".format(event_name=ev.event_name)
        eventStr += "\"start\": new Date({yy}, {mm}, {dd}, {hh}, {min}),  ".format(yy=ev.start_time.year,
                                                                                   mm=ev.start_time.month - 1,
                                                                                   dd=ev.start_time.day,
                                                                                   hh=ev.start_time.hour,
                                                                                   min=ev.start_time.minute)
        eventStr += "\"end\": new Date({yy}, {mm}, {dd}, {hh}, {min}),  ".format(yy=ev.end_time.year,
                                                                                 mm=ev.end_time.month - 1,
                                                                                 dd=ev.end_time.day,
                                                                                 hh=ev.end_time.hour,
                                                                                 min=ev.end_time.minute)
        eventStr += "\"id\": {event_id},  ".format(event_id=ev.event_id)
        eventStr += "\"allDay\": false,  "
        eventStr += "\"className\": \"success\",  "
        eventStr += "\"description\": \"{description}\",  ".format(description=ev.description)
        # this url field needs to be modified
        eventStr += "\"url\": \"{url}\"".format(url=ev.get_html_url)
        eventStr += "},"
    if len(eventStr) > 1:
        eventStr = eventStr[:-1]
    eventStr += "]"
    return eventStr


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
    instance.time_of_edit = datetime.now()
    print(instance.time_of_edit)
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
    return render(request, 'accounts/profile.html')
