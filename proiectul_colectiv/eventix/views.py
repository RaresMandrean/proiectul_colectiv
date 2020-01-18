from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


from eventix.models import Event, Seat
from eventix.forms import EventForm
from users.models import CustomUser


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


def about(request):
    return render(request, 'eventix/about.html', {'title': 'About'})
