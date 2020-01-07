from django.core.exceptions import ObjectDoesNotExist
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

    def get_queryset(self):
        filter = self.request.GET.get('text_filter', '')
        return Event.objects.filter(Q(title__icontains=filter))


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
