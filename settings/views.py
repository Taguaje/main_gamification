from django.db.models import QuerySet
from django.shortcuts import render

from settings.models import LMSEvents
from .models import LMS, LMSUsers, LMSEvents, EventPoints, LevelOption
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

    if lms.MaxPoints == None:
        maxPoints = "не задано"
    else:
        maxPoints = lms.MaxPoints
    events = LMSEvents.objects.filter(lms=lms)
    eventlist = []
    for event in events:
        if lms.PointsIsOn:
            try:
                points = EventPoints.objects.get(event=event, lms=lms)
            except EventPoints.DoesNotExist:
                point = 'задать'
                eventlist.append((event, point))
            else:
                point = points.points
                eventlist.append((event, point))
        else:
            eventlist.append((event,))

    return render(request, 'settings/lms_events.html', {'form1': form_create, 'events': eventlist, 'pointIsOn': lms.PointsIsOn, 'maxPoints': maxPoints})


def delete_event(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        event = LMSEvents.objects.get(id = id)
        event.delete()
        return HttpResponse('ok', content_type='text/html')


def turn_points_on(request):
    if request.method == 'POST':
        try:
            users_lms = LMSUsers.objects.get(user=request.user)
        except LMSUsers.DoesNotExist:
            return HttpResponse('fail', content_type='text/html')
        else:
            lms = users_lms.lms
            lms.PointsIsOn = True
            lms.save()
            return HttpResponse('ok', content_type='text/html')


def turn_points_off(request):
    if request.method == 'POST':
        try:
            users_lms = LMSUsers.objects.get(user=request.user)
        except LMSUsers.DoesNotExist:
            return HttpResponse('fail', content_type='text/html')
        else:
            lms = users_lms.lms
            lms.PointsIsOn = False
            lms.save()
            return HttpResponse('ok', content_type='text/html')


def set_max_points(request):
    if request.method == 'POST':
        try:
            users_lms = LMSUsers.objects.get(user=request.user)
        except LMSUsers.DoesNotExist:
            return HttpResponseRedirect('/settings/events')
        else:
            maxpoints = request.POST.get('maxpoints')
            lms = users_lms.lms
            lms.MaxPoints = maxpoints
            lms.save()
            return HttpResponseRedirect('/settings/events')

def levels(request):
    try:
        users_lms = LMSUsers.objects.get(user=request.user)
    except LMSUsers.DoesNotExist:
        return HttpResponseRedirect('/settings')
    lms = users_lms.lms
    if lms.MaxLevel == None:
        maxLevel = "не задано"
    else:
        maxLevel = lms.MaxLevel
    events = LMSEvents.objects.filter(lms=lms)
    options = LevelOption.objects.filter(lms=lms)

    return render(request, 'settings/lms_levels.html',{'maxLevel': maxLevel, 'events': events, 'options': options})


def set_max_level(request):
    if request.method == 'POST':
        try:
            users_lms = LMSUsers.objects.get(user=request.user)
        except LMSUsers.DoesNotExist:
            return HttpResponseRedirect('/settings/levels')
        else:
            maxlevel = request.POST.get('maxlevel')
            lms = users_lms.lms
            lms.MaxLevel = maxlevel
            lms.save()
            return HttpResponseRedirect('/settings/levels')

def add_level_option(request):
    if request.method == 'POST':
        try:
            users_lms = LMSUsers.objects.get(user=request.user)
        except LMSUsers.DoesNotExist:
            return HttpResponseRedirect('/settings/levels')
        else:
            eventid = request.POST.get('event')
            try:
                event = LMSEvents.objects.get(id=eventid)
            except LMSEvents.DoesNotExist:
                return HttpResponseRedirect('/settings/levels')
            else:
                amount = request.POST.get('amount')
                if int(amount) != 0 and amount != None:
                    lms = users_lms.lms
                    option = LevelOption()
                    option.lms = lms
                    option.event = event
                    option.amount = amount
                    option.isActive = True
                    option.save()
                    return HttpResponseRedirect('/settings/levels')


def delete_option(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        option = LevelOption.objects.get(id = id)
        option.delete()
        return HttpResponse('ok', content_type='text/html')


def set_level_amount(request):
    if request.method == 'POST':
        id = request.POST.get('cur_option')
        try:
            option = LevelOption.objects.get(id=id)
        except LevelOption.DoesNotExist:
            return HttpResponseRedirect('/settings/levels')
        else:
            amount = request.POST.get('amountnew')
            if amount == None:
                return HttpResponseRedirect('/settings/levels')
            else:
                option.amount = amount
                option.save()
                return HttpResponseRedirect('/settings/levels')


def turnoff_level(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        option = LevelOption.objects.get(id = id)
        option.isActive = False
        option.save()
        return HttpResponse('ok', content_type='text/html')


def turnon_level(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        option = LevelOption.objects.get(id = id)
        option.isActive = True
        option.save()
        return HttpResponse('ok', content_type='text/html')