from django.shortcuts import render
from .models import LMS,LMSUsers
from .forms import LMSChangeNameForm,LMSCreateForm
from django.http import HttpResponseRedirect

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
