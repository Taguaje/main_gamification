from django.shortcuts import render


def index(request):
    return render(request, 'home_page/main_page.html', {})
