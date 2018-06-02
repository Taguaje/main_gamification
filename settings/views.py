from django.db.models import QuerySet
from django.shortcuts import render
from .models import LMS, LMSUsers, LMSEvents, EventPoints, LevelOptions, Parameters, Badges
from .forms import LMSChangeNameForm, LMSCreateForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse


# главная страница настройки компонентов игрофикации
def index(request):

    # проверяем создана ли LMS для пользователя
    try:
        users_lms = LMSUsers.objects.get(user=request.user)
    except LMSUsers.DoesNotExist:
        lmsname = 'не создана'
    else:
        lms = users_lms.lms
        lmsname = lms.Name

    if request.method == 'POST':
        # если не LMS не создана, создаем новую и связывыем ее с пользователем
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
            # поменяем имя LMS
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


# страница настройки событий
def events(request):
    try:
        users_lms = LMSUsers.objects.get(user=request.user)
    except LMSUsers.DoesNotExist:
        return HttpResponseRedirect('/settings')

    lms = users_lms.lms
    if request.method == 'POST':
        form_create = EventForm(request.POST)
        if form_create.is_valid():
            event = LMSEvents()
            event.name = form_create.cleaned_data['name']
            event.lms = lms
            event.save()
            return HttpResponseRedirect('/settings/events')
    else:
        form_create = EventForm

    if lms.MaxPoints is None:
        max_points = "не задано"
    else:
        max_points = lms.MaxPoints

    events_original = LMSEvents.objects.filter(lms=lms)
    event_list = []
    for event in events_original:
        if lms.PointsIsOn:
            try:
                points = EventPoints.objects.get(event=event, lms=lms)
            except EventPoints.DoesNotExist:
                point = 'задать'
                event_list.append((event, point))
            else:
                point = points.points
                event_list.append((event, point))
        else:
            event_list.append((event,))

    data = {'form': form_create, 'events': event_list, 'pointIsOn': lms.PointsIsOn, 'maxPoints': max_points}
    return render(request, 'settings/lms_events.html', data)


# задаем  количество очков для события
def set_event_points(request):
    try:
        users_lms = LMSUsers.objects.get(user=request.user)
    except LMSUsers.DoesNotExist:
        return HttpResponseRedirect('/settings')
    lms = users_lms.lms

    if request.method == 'POST':
        event_id = request.POST.get('event')
        try:
            event = LMSEvents.objects.get(id=event_id)
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
                event_points.save()
            return HttpResponseRedirect('/settings/events')


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
    options = LevelOptions.objects.filter(lms=lms)

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
                    option = LevelOptions()
                    option.lms = lms
                    option.event = event
                    option.amount = amount
                    option.isActive = True
                    option.save()
                    return HttpResponseRedirect('/settings/levels')


def delete_option(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        option = LevelOptions.objects.get(id = id)
        option.delete()
        return HttpResponse('ok', content_type='text/html')


def set_level_amount(request):
    if request.method == 'POST':
        id = request.POST.get('cur_option')
        try:
            option = LevelOptions.objects.get(id=id)
        except LevelOptions.DoesNotExist:
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
        option = LevelOptions.objects.get(id = id)
        option.isActive = False
        option.save()
        return HttpResponse('ok', content_type='text/html')


def turnon_level(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        option = LevelOptions.objects.get(id = id)
        option.isActive = True
        option.save()
        return HttpResponse('ok', content_type='text/html')


def badges(request):
    try:
        users_lms = LMSUsers.objects.get(user=request.user)
    except LMSUsers.DoesNotExist:
        return HttpResponseRedirect('/settings')
    else:
        lms = users_lms.lms
        events = LMSEvents.objects.filter(lms=lms)
        parameters = Parameters.objects.filter(lms=lms)
        badgelist = Badges.objects.filter(lms=lms)
        return render(request, 'settings/lms_badges.html',{'events': events, 'parameters': parameters, 'badges': badgelist})

def add_parameter(request):
    if request.method == 'POST':
        try:
            users_lms = LMSUsers.objects.get(user=request.user)
        except LMSUsers.DoesNotExist:
            return HttpResponseRedirect('/settings')
        else:
            lms = users_lms.lms
            eventid = request.POST.get('event')
            try:
                event = LMSEvents.objects.get(id=eventid)
            except LMSEvents.DoesNotExist:
                event = None
            name = request.POST.get('name')
            parameter = Parameters()
            parameter.lms = lms
            parameter.event = event
            parameter.name = name
            parameter.save()
            return HttpResponseRedirect('/settings/badges')


def add_badge(request):
    if request.method == 'POST':
        try:
            users_lms = LMSUsers.objects.get(user=request.user)
        except LMSUsers.DoesNotExist:
            return HttpResponseRedirect('/settings')
        else:
            lms = users_lms.lms
            name = request.POST.get('name')
            parameterid = request.POST.get('parameter')
            parameter = Parameters.objects.get(id=parameterid)
            comparison = request.POST.get('comparison')
            criteria = request.POST.get('criteria')
            img = request.POST.get('badge')

            badge = Badges()
            badge.lms = lms
            badge.parameter = parameter
            badge.comparison_type = comparison
            badge.criterion = criteria
            badge.name = name
            badge.isActive = True
            badge.img = img
            badge.save()
            return HttpResponseRedirect('/settings/badges')


def delete_badge(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        badge = Badges.objects.get(id=id)
        badge.delete()
        return HttpResponse('ok', content_type='text/html')


def turnoff_badge(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        badge = Badges.objects.get(id = id)
        badge.isActive = False
        badge.save()
        return HttpResponse('ok', content_type='text/html')


def turnon_badge(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        badge = Badges.objects.get(id=id)
        badge.isActive = True
        badge.save()
        return HttpResponse('ok', content_type='text/html')


def delete_parameter(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        parameter = Parameters.objects.get(id=id)
        parameter.delete()
        return HttpResponse('ok', content_type='text/html')