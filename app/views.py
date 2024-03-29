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
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.forms.models import model_to_dict
import simplejson

from .models import *
from .forms import EventForm

import environ
import json

from .utils import search_result, get_event_str

env = environ.Env()


def index(request):
    if request.user.is_authenticated:
        return redirect('/logout/')
    context = search_result(request)
    return render(request, 'index.html', context)


@login_required
def event(request, event_id=None):
    if request.user.verification_status == False:
        return render(request, 'event_add_and_edit.html', {'verification_status': False})
    if event_id:
        event = Event.objects.get(event_id=event_id)
        subject = Subject.objects.get(subject_id=getattr(event,'subject_id'))
        # subject = subject.values(())
        subject = {
            'subject_code_name': subject.subject_code+' - '+subject.subject_name,
            'year': subject.year,
            'semester': subject.semester
        }
        st_time=str(event.start_time)
        event.start_time='T'.join(st_time[:-9].split(' '))
        e_time=str(event.end_time)
        event.end_time='T'.join(e_time[:-9].split(' '))
        print(subject,event.is_recurring)
        return render(request, 'event_add_and_edit.html', {'event': event, 'subject':subject})
    elif request.POST:
        data=request.POST.copy()
        print(data)
        # data['subject']=' '.join(data['subject'].split(' '))
        sub=Subject.objects.get(subject_code=data['subject'][:7])
        data['subject']=sub

        instance=Event()
        instance.time_of_edit = timezone.now()
        instance.user=request.user
        instance.subject=sub

        form = EventForm(data or None, instance=instance)

        if form.is_valid():
            form.save()
            msg='Event added successfully!'
        return render(request, 'event_add_and_edit.html', {'msg': msg, 'form':form})
    else:
        return render(request, 'event_add_and_edit.html')

def event_view(request, event_id=None):
    event = Event.objects.get(event_id=event_id)
    subject = Subject.objects.get(subject_id = getattr(event,'subject_id'))
    return render(request, 'event.html',{'event': event, 'subject_name':getattr(subject,'subject_name')+" ("+getattr(subject,'subject_code')+")"})

def instructions(request):
    return render(request, 'instructions.html')


def about_us(request):
    return render(request, 'about_us.html')


@login_required
def add_registered_subject(request):
    if request.is_ajax():
        data=request.POST
        print(data)
        sub=Subject.objects.filter(subject_code=data['subject'][:7])
        if not sub:
            response={
                'flag' : 'failed',
                'message' : 'Subject not available!'
            }
        else:
            resp=RegisteredSubjects.objects.update_or_create(user=request.user, subject=sub[0])
            print(resp)
            if resp[1]:
                registered_subjects=Subject.objects.filter(subject_id=resp[0].subject_id)
                events = Event.objects.filter(subject__in=registered_subjects)
                # print(events.values())
                response={
                    'flag' : 'success',
                    'message' : 'Subject added successfully!',
                    'event' : get_event_str(events),
                    'subject_id' : str(resp[0].subject_id)
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
def delete_registered_subject(request):
    if request.is_ajax():
        data=request.POST
        print("data---->",data,data['subject_id'][27:])
        sub=Subject.objects.get(subject_id=data['subject_id'][27:])
        # if not sub:
        #     response={
        #         'flag' : 'failed',
        #         'message' : 'Subject not available!'
        #     }
        # else:
        resp=RegisteredSubjects.objects.get(user=request.user, subject=sub)
        resp.delete()
        response={
            'flag' : 'success',
            'message' : 'Subject deleted successfully!',
            # 'event' : get_event_str(events),
            # 'subject_id' : str(resp[0].subject_id)
        }
    else:
        respons={}
    json = simplejson.dumps(response)
    return HttpResponse(json, content_type="text/json")


@login_required
def my_subjects(request):
    context={}
    registered_subject_ids=RegisteredSubjects.objects.filter(user=request.user)
    registered_subjects=Subject.objects.filter(subject_id__in=registered_subject_ids.values('subject_id'))
    registered_subjects_min=registered_subjects.values('subject_code','subject_name','subject_id')
    print(registered_subjects_min)
    context['registered_subjects']=registered_subjects_min


    events = Event.objects.filter(subject__in=registered_subjects)
    # print(events.values())
    context['event'] = get_event_str(events)
    print(context['event'])
    return render(request, 'my_subjects.html', context)


@login_required
def userhome(request):
    context = search_result(request)
    return render(request, 'userindex.html', context)


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
