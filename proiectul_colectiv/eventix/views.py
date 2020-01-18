from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from eventix.forms import EventForm
from eventix.models import Event
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
