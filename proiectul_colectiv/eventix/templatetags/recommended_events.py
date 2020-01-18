from django import template
import pandas as pd

from eventix.models import Event

register = template.Library()


@register.filter(name="recommended_events")
def get_recommended_events(user):
    recommended_events = []
    df = pd.read_csv('ai_data/Results.csv')
    if user.pk:
        user_id = user.pk
        df = df.loc[df['USER_ID'] == user_id - 1, ['TOP_1_EVENT_ID', 'TOP_1_RATING', 'TOP_2_EVENT_ID', 'TOP_2_RATING', 'TOP_3_EVENT_ID', 'TOP_3_RATING', 'TOP_4_EVENT_ID', 'TOP_4_RATING', 'TOP_5_EVENT_ID', 'TOP_5_RATING']]
        print(df)
        for index, row in df.iterrows():
            for i in range(0, 5):
                event = Event.objects.get(pk=row['TOP_' + str(i+1) + '_EVENT_ID'] + 1)
                recommended_events.append(event)
            break
    for event in recommended_events:
        print(str(event.pk) + "------" + event.title + "--------" + str(event.date_posted))
    return recommended_events




