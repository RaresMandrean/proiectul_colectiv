from django.db import models
from django.utils import timezone
from django.urls import reverse

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})
