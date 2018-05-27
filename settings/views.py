from django.db.models import QuerySet
from django.shortcuts import render

from settings.models import LMSEvents
from .models import LMS, LMSUsers, LMSEvents, EventPoints
from .forms import LMSChangeNameForm, LMSCreateForm, EventCreate
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    try:
        users_lms = LMSUsers.objects.get(user=request.user)
    except LMSUsers.DoesNotExist:
        lmsname = 'не создана'
    else:
        lms = users_lms.lms
        lmsname = lms.Name

    if request.method == 'POST':
        if lmsname == 'не создана':
            form = LMSCreateForm(request.POST)
            if form.is_valid():
                lms = form.save()
                lms_user = LMSUsers()
                lms_user.lms = lms
                lms_user.user = request.user
                lms_user.save()
                return HttpResponseRedirect('/settings')
        else:
            form = LMSChangeNameForm(request.POST, instance=lms)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/settings')
    else:
        if lmsname == 'не создана':
            form = LMSCreateForm
        else:
            form = LMSChangeNameForm(instance=lms)

    return render(request,'settings/index.html',{'lms':lmsname, 'form': form})


def events(request):
    try:
        users_lms = LMSUsers.objects.get(user=request.user)
    except LMSUsers.DoesNotExist:
        return HttpResponseRedirect('/settings')

    lms = users_lms.lms
    if request.method == 'POST':
        if request.POST.get('event') != None:
            eventid = request.POST.get('event')
            try:
                event = LMSEvents.objects.get(id=eventid)
            except LMSEvents.DoesNotExist:
                return HttpResponseRedirect('/settings/events')
            else:
                try:
                    event_points = EventPoints.objects.get(event=event, lms=lms)
                except EventPoints.DoesNotExist:
                    event_points = EventPoints()
                    event_points.lms = lms
                    event_points.event = event
                    event_points.points = request.POST.get('points')
                    event_points.save()
                else:
                    event_points.points = request.POST.get('points')
                    event_points.points = request.POST.get('points')
                    event_points.save()
                return HttpResponseRedirect('/settings/events')

        form_create = EventCreate(request.POST)
        if form_create.is_valid():
            event = LMSEvents()
            event.name = form_create.cleaned_data['name']
            event.lms = lms
            event.save()
            return HttpResponseRedirect('/settings/events')
    else:
        form_create = EventCreate

    events = LMSEvents.objects.filter(lms=lms)
    eventlist = []
    for event in events:
        try:
            points = EventPoints.objects.get(event=event, lms=lms)
        except EventPoints.DoesNotExist:
            point = 'задать'
            eventlist.append((event, point))
        else:
            point = points.points
            eventlist.append((event, point))

    return render(request, 'settings/lms_events.html', {'form1': form_create, 'events': eventlist})


def delete_event(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        event = LMSEvents.objects.get(id = id)
        event.delete()
        return HttpResponse('ok', content_type='text/html')
