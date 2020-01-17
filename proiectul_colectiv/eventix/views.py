from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from eventix.models import Event, Seat, Location
from eventix.forms import EventForm
from users.models import CustomUser
import json


def home(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'eventix/home.html', context)


class EventListView(ListView):
    model = Event
    template_name = 'eventix/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'events'
    ordering = ['-date_posted']
    paginate_by = 5


class UserEventListView(ListView):
    model = Event
    template_name = 'eventix/user_events.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'events'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        return Event.objects.filter(organiser=user).order_by('-date_posted')


class EventDetailView(DetailView):
    model = Event

    def is_going(self):
        try:
            Seat.objects.get(location=self.object.location, reserved_to=self.request.user)
            return True
        except ObjectDoesNotExist as e:
            return False


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.organiser = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.organiser = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.organiser:
            return True
        return False


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.organiser:
            return True
        return False

class EventAddSeatsLocation(LoginRequiredMixin, CreateView):
    model = Location
    form_class = EventForm
    def form_valid(self,request):
        print("INTRA AICI2")
        if request.is_ajax():
            print(request.POST)
            #location = Location.objects.create_location("asdsa", "asda", "asdas", 123)
            #location=Location.objects.create(name="sasd",city="asdas",address="dsasda",maximum_number_of_seats=200)
            #print(location)
            return render(request, 'eventix/event_form.html', {'title': 'event-addSeatsLocation'})
        return render(request, 'eventix/event_form.html', {'title': 'event-addSeatsLocation'})

def eventAddSeatsLocation(request):
    if request.is_ajax():
        print(request.POST)
        requestString=""
        for x in request.POST.dict():
            requestString=x
        print(requestString)
        print(json.loads(requestString)[0]["name"])
        requestJSON=json.loads(requestString)
        location = Location.objects.create(name=requestJSON[0]["name"], city=requestJSON[0]["city"], address=requestJSON[0]["address"], maximum_number_of_seats=requestJSON[0]["maximum_number_of_seats"])
        for i in range(1, len(requestJSON)):
            Seat.objects.create(position=requestJSON[i]["position"],location=location,price=requestJSON[i]["price"],special_seat=requestJSON[i]["special_seat"])
        #position,location,price,reserved_to,special_seat
        return render(request, 'eventix/event_form.html', {'title': 'event-addSeatsLocation'})
    return render(request, 'eventix/event_form.html', {'title': 'event-addSeatsLocation'})

def about(request):
    return render(request, 'eventix/about.html', {'title': 'About'})
