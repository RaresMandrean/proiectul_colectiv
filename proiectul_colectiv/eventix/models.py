from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.urls import reverse
from star_ratings.models import Rating

from users.models import CustomUser


class Location(models.Model):  # asta ar fi sala
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    maximum_number_of_seats = models.IntegerField()

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateField(default=timezone.now)
    organiser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    event_date = models.DateField()
    pending_approval = models.BooleanField(default=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    ratings = GenericRelation(Rating)
    poster = models.ImageField(upload_to="event_posters", blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class Seat(models.Model):
    position = models.PositiveIntegerField()
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    reserved_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    special_seat = models.BooleanField(default=False)  # devine gri si nu poate fi selectat daca e True pe "harta"
