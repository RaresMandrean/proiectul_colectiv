import random

import pandas as pd
from django.contrib.auth.models import User

from eventix.models import Location, Event


def read_data(filename):
    df = pd.read_csv(filename)
    return df


def add_locations_to_db():
    df = read_data("ai_data/Locations.csv")
    for index, row in df.iterrows():
        location = Location()
        location.name = row['NAME']
        location.city = row['CITY']
        location.address = row['ADDRESS']
        location.maximum_number_of_seats = random.randint(20, 1000)
        location.save()


def add_events_to_db():
    df = read_data("ai/Events.csv")
    for index, row in df.iterrows():
        event = Event()
        event.title = row['TITLE']
        event.content = row['CONTENT']
        event.date_posted = row['DATE_POSTED']
        event.organiser = row['ORGANIZER']
        event.approved = row['APPROVED']
        event.event_date = row['EVENT_DATE']
        event.pending_approval = row['PENDING_APPROVAL']
        event.location = row['LOCATION']
        event.save()


def add_users_to_db():
    df = read_data("ai/Users.csv")
    for index, row in df.ierroows():
        user = User()
        user.username = row['USERNAME']
        user.password = 'test12345'
        user.first_name = row['FIRST_NAME']
        user.last_name = row['LAST_NAME']
        user.email = row['EMAIL']
        user.date_joined = row['DATE_JOINED']
        user.save()
