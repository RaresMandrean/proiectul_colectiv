from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    UserEventListView,
    OrganiserListView,
    change_organiser_status,
    join_event
)
from . import views

urlpatterns = [
    path('', EventListView.as_view(), name='eventix-home'),
    path('user/<str:username>', UserEventListView.as_view(), name='user-events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('event/<int:pk>/join/', join_event, name='join-event'),
    path('organisers/', OrganiserListView.as_view(), name='event-organisers'),
    path('organisers/organiser-status/', change_organiser_status, name='organiser-status'),
    path('event/new/EventAddSeatsLocation', views.eventAddSeatsLocation, name='event-addSeatsLocation'),
    path('about/', views.about, name='eventix-about'),
]
