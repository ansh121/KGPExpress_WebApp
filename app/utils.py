from .forms import *
from .models import *
from django.forms.models import model_to_dict


def search_result(request):
    context={}
    context['search_result']=False

    form = SearchForm(request.GET or None)
    subList = []
    if form.is_valid():
        context['search_result']=True
        query_code= form.cleaned_data['subject'][:7]
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

    events = Event.objects.filter(subject__in=subList)
    context['event'] = get_event_str(events)
    context['form'] = form
    if subList:
        sub_dict = model_to_dict(subList[0])
        sub_dict.pop('subject_id')
        sub_dict.pop('semester')
        sub_dict.pop('year')
        sub_dict_new_keys={}
        for k,v in sub_dict.items():
            sub_dict_new_keys[k.replace('_',' ')]=v
        context['subject_details'] = sub_dict_new_keys
        print(sub_dict_new_keys)

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
        eventStr += "\"url\": \"{url}\"".format(url="")
        eventStr += "},"
    if len(eventStr) > 1:
        eventStr = eventStr[:-1]
    eventStr += "]"
    return eventStr