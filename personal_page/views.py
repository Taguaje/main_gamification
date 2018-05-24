from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import ChangeEmailForm
from django.urls import reverse, resolve


def index(request):
    current_user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            current_user.email = form.cleaned_data['email']
            current_user.save()
            return HttpResponseRedirect('/profile/')
    else:
        form = ChangeEmailForm

    email = current_user.email
    if email == "":
        useremail = "не задан"
    else:
        useremail = email

    return render(request, 'personal_page/index.html', {'email':useremail, 'form': form})
