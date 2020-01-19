from django import template

register = template.Library()


@register.filter
def count_none(value):
    counter = 0
    for element in value:
        if not element.poster:
            counter += 1
    return counter
