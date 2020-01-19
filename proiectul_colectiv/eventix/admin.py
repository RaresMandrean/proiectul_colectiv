from django.contrib import admin
from .models import Event, Seat, Location, UserEvent

admin.site.register(Event)
admin.site.register(Seat)
admin.site.register(Location)
admin.site.register(UserEvent)
