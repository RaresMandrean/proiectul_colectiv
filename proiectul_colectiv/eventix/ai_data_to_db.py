from datetime import datetime
import random

import pandas as pd
import pytz

from eventix.models import Location, Event
from users.models import CustomUser


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
        location.height = random.randint(20, 1000)
        location.width = random.randint(20, 1000)
        location.save()


def add_events_to_db():
    df = read_data("ai_data/Events.csv")
    for index, row in df.iterrows():
        event = Event()
        event.title = row['TITLE']
        event.content = row['CONTENT']
        event.date_posted = datetime.strptime(row['DATE_POSTED'], '%d-%m-%Y').strftime('%Y-%m-%d')
        event.organiser = CustomUser.objects.get(id=1)
        event.approved = row['APPROVED']
        event.event_date = row['EVENT_DATE']
        event.pending_approval = row['PENDING_APPROVAL']
        event.location = Location.objects.get(id=row['LOCATION'] + 1)
        event.save()


def add_users_to_db():
    df = read_data("ai_data/1000Users.csv")
    for index, row in df.iterrows():
        CustomUser.objects.create_user(row['USERNAME'], password='test12345', first_name=row['FIRST_NAME'], last_name=row['LAST_NAME'], email=row['EMAIL'], date_joined=datetime.now(pytz.utc), is_organiser=True)


add_users_to_db()
add_locations_to_db()
add_events_to_db()
print("Finished migrating data from csv to db")
