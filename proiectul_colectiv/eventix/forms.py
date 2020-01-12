from datetime import datetime

from django import forms
from django.utils import timezone
from django.core.files.images import get_image_dimensions

from eventix.models import Event, Location, Seat


class EventForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    event_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Event
        fields = ('title', 'content', 'event_date', 'location', 'poster')

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date < datetime.date(timezone.now()):
            raise forms.ValidationError("You cannot set an event in the past!")
        return event_date

    def clean(self):
        location = self.cleaned_data.get('location')
        event_date = self.cleaned_data.get('event_date')
        for event in Event.objects.filter(location=location):
            if event.event_date == event_date:
                raise forms.ValidationError("This location is already reserved for another event on that date!")
        return super().clean()

    def clean_poster(self):
        poster = self.cleaned_data.get('poster')
        width, height = get_image_dimensions(poster)
        if width < 500 or height < 550:
            raise forms.ValidationError("Minimum poster resolution should be 500x550px")
        return poster


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ('position', 'price', 'special_seat')

    def clean(self):
        position = self.cleaned_data.get('position')
        location = self.cleaned_data.get('location')
        for seat in Seat.objects.fitler(location=location):
            if position == seat.position:
                raise forms.ValidationError("There is already a seat with this number!")
        return super().clean()
