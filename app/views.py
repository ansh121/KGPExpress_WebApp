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
from django.core.exceptions import ValidationError
from django.utils import timezone
import calendar
import simplejson

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
        # d = get_date(self.request.GET.get('month', None))
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
        # print(context['event'])
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


# def get_date(req_month):
#     if req_month:
#         year, month = (int(x) for x in req_month.split('-'))
#         return date(year, month, day=1)
#     return datetime.today()


# def prev_month(d):
#     first = d.replace(day=1)
#     prev_month = first - timedelta(days=1)
#     month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
#     return month


# def next_month(d):
#     days_in_month = calendar.monthrange(d.year, d.month)[1]
#     last = d.replace(day=days_in_month)
#     next_month = last + timedelta(days=1)
#     month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
#     return month


@login_required
def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
        form = EventForm(request.POST or None, instance=instance)
        return render(request, 'event.html', {'form': form})
    elif request.POST:
        data=request.POST.copy()
        sub=Subject.objects.get(subject_code=data['subject'][:7])
        data['subject']=sub

        instance=Event()
        instance.time_of_edit = timezone.now()
        instance.user=request.user
        instance.subject=sub

        form = EventForm(data or None, instance=instance)

        if form.is_valid():
            # print(form)
            form.save()
            return HttpResponseRedirect(reverse('app:event_new'))
        return render(request, 'event.html', {'form': form})
    else:
        return render(request, 'event.html')


def instructions(request):
    return render(request, 'instructions.html')


def about_us(request):
    return render(request, 'about_us.html')


@login_required
def add_registered_subject(request):
    if request.is_ajax():
        data=request.POST
        sub=Subject.objects.filter(subject_code=data['subject'][:7])
        if not sub:
            response={
                'flag' : 'failed',
                'message' : 'Subject not available!'
            }
        else:
            resp=RegisteredSubjects.objects.update_or_create(user=request.user, subject=sub[0])
            print(resp[1])
            if resp[1]:
                response={
                    'flag' : 'success',
                    'message' : 'Subject added successfully!'
                }
            else:
                response={
                    'flag' : 'failed',
                    'message' : 'Subject already added!'
                }
    else:
        respons={}
    json = simplejson.dumps(response)
    return HttpResponse(json, content_type="text/json")


@login_required
def add_registered_subject(request):
    if request.is_ajax():
        data=request.POST
        sub=Subject.objects.filter(subject_code=data['subject'][:7])
        if not sub:
            response={
                'flag' : 'failed',
                'message' : 'Subject not available!'
            }
        else:
            resp=RegisteredSubjects.objects.update_or_create(user=request.user, subject=sub[0])
            print(resp[1])
            if resp[1]:
                response={
                    'flag' : 'success',
                    'message' : 'Subject added successfully!'
                }
            else:
                response={
                    'flag' : 'failed',
                    'message' : 'Subject already added!'
                }
    else:
        respons={}
    json = simplejson.dumps(response)
    return HttpResponse(json, content_type="text/json")


@login_required
def my_subjects(request):
    context={}
    registered_subject_ids=RegisteredSubjects.objects.filter(user=request.user)
    registered_subjects=Subject.objects.filter(subject_id__in=registered_subject_ids)
    registered_subjects=registered_subjects.values('subject_code','subject_name')
    print(registered_subjects)
    context['registered_subjects']=registered_subjects
    return render(request, 'my_subjects.html', context)

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
            if v[0]:
                initial_data[k]=v[0]
        print(initial_data)

        # user=CustomUser.objects.update_or_create(initial_data)
        # user.save()
        user=CustomUser(initial_data)
        try:
            user.full_clean()
        except ValidationError:
            # Do something when validation is not passing
            print(ValidationError)
        else:
            # Validation is ok we will save the instance
            user.save()

        # if user.full_clean():
        #     user.save()
        
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
