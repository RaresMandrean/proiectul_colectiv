from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django import utils

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from eventix.forms import EventForm
from eventix.models import Event, Seat, Location, UserEvent
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

    def get(self, request, *args, **kwargs):
        events = self.apply_filter(Event.objects.all(), request.GET)

        paginator = Paginator(events, self.paginate_by)
        page = request.GET.get('page')

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context = {
            'events': events
        }
        return render(request, "eventix/home.html", context)

    def apply_filter(self, events, filters):
        # get filters
        text_filter = filters.get('text_filter')
        organiser_name = filters.get('organiser_name')
        location_name = filters.get('location_name')
        minimum_rating = filters.get('minimum_rating')
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')

        # if advanced filters are applied, apply the text filter only on title and content
        if text_filter:
            events = events.filter(Q(title__icontains=text_filter) |
                                   Q(content__icontains=text_filter))
        if organiser_name:
            events = events.filter(Q(organiser__first_name__icontains=organiser_name) |
                                   Q(organiser__last_name__icontains=organiser_name) |
                                   Q(organiser__username__icontains=organiser_name))
        if location_name:
            events = events.filter(Q(location__name__icontains=location_name) |
                                   Q(location__city__icontains=location_name) |
                                   Q(location__address__icontains=location_name))
        if minimum_rating:
            events = events.filter(Q(ratings__average__gte=minimum_rating))
        if start_date:
            events = events.filter(Q(event_date__gte=start_date))
        if end_date:
            events = events.filter(Q(event_date__lte=end_date))

        return events


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
            Seat.objects.get(location=self.object.location)
            return True
        except ObjectDoesNotExist as e:
            return False


class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.organiser = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name__in=[settings.APPROVED_ORGANISERS]).exists()


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
class EventSeatsListView(LoginRequiredMixin, ListView):
    model = Seat
    def get_queryset(self):
        lista = Seat.objects.all()
        lista=[]
        for i in Seat.objects.all:
            lista.append(i)
        json_list = utils.simplejson.dumps(lista)
        return render("eventix/join_event", {'list_objects':lista})

class EventListEventUserView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_variable = "userevents"

class EventSendEventToJoinView(LoginRequiredMixin):
    model = Event
    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs.get('pk'))
        return event

def join_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    seats = Seat.objects.all().filter(location=event.location)
    return render(request, 'eventix/join_event.html', {
        'event': event,
        'seats': seats,
    })

def join_event_toDB(request,pk):
    if request.is_ajax():
        eventid=request.GET.get("eventId")
        locationName=request.GET.get("location")
        position=request.GET.get("position")
        price=request.GET.get("price")
        location=get_object_or_404(Location, name=locationName)
        event=get_object_or_404(Event, id=pk)
        seat=get_object_or_404(Seat, location=location, position=position)
        Seat.objects.filter(id=seat.id).update(special_seat=True)
        UserEvent.objects.create(user=request.user, event=event, seat=seat, price=price)
        return HttpResponse("")
    return HttpResponse("")

def eventAddSeatsLocation(request):
    if request.is_ajax():
        requestString = ""
        for x in request.POST.dict():
            requestString = x
        requestJSON = json.loads(requestString)
        location = Location.objects.create(name=requestJSON[0]["name"], city=requestJSON[0]["city"],
                                           address=requestJSON[0]["address"],
                                           width=requestJSON[0]["width"], height=requestJSON[0]["height"])
        for i in range(1, len(requestJSON)):
            Seat.objects.create(position=requestJSON[i]["position"], location=location, price=requestJSON[i]["price"],
                                special_seat=requestJSON[i]["special_seat"])
        return render(request, 'eventix/event_form.html', {'title': 'event-addSeatsLocation'})
    return render(request, 'eventix/event_form.html', {'title': 'event-addSeatsLocation'})


def add_user_to_event(request, pk):
    if request.method == 'GET':
        current_user = request.user
        event = get_object_or_404(Event, id=pk)
        return HttpResponse(status=200)
    return HttpResponse('User cannot join the event')


class OrganiserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'eventix/event_organisers.html'
    paginate_by = 5

    def get_queryset(self):
        return CustomUser.objects.filter(is_organiser=True).order_by('-date_joined')


@user_passes_test(lambda u: u.is_superuser)
def change_organiser_status(request):
    username = request.GET.get('username')
    status = request.GET.get('status')
    user = get_object_or_404(CustomUser, username=username)
    try:
        approved_group = Group.objects.get(name=settings.APPROVED_ORGANISERS)
        rejected_group = Group.objects.get(name=settings.REJECTED_ORGANISERS)
        user.groups.remove(rejected_group)
        user.groups.remove(approved_group)
        if status == 'approved':
            user.groups.add(approved_group)
        else:
            user.groups.add(rejected_group)
    except Group.DoesNotExist:
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def about(request):
    return render(request, 'eventix/about.html', {'title': 'About'})
