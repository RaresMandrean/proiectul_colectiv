from django import template

from eventix.models import Seat, UserEvent

register = template.Library()


@register.filter(name="seats_list")
def seats_list(seats):
    lista=[]
    for seat in seats:
        jsonString={"position": seat.position,"price":seat.price, "special_seat": str(seat.special_seat).lower()}
        lista.append(jsonString)
    return lista

@register.filter(name="reserved_list")
def reserved_list(user, event):
    users_event=UserEvent.objects.all()

    is_reserved = "'not reserved'"
    for user_event in users_event:
        if user_event.user.username == user.username and user_event.seat != None and user_event.event.title == event.title:
            is_reserved = {
                "position": user_event.seat.position,
                "price": user_event.seat.price,
                "special_seat": str(user_event.seat.special_seat).lower()
            }
    return is_reserved

@register.filter(name="one_more")
def one_more(unu, doi):
    return unu, doi