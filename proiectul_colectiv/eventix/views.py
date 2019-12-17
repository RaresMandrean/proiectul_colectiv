from django.shortcuts import render
from .models import Event


def home(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'eventix/home.html', context)


def about(request):
    return render(request, 'eventix/about.html', {'title': 'About'})