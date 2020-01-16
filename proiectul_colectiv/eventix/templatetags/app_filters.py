from django import template

register = template.Library()

@register.filter
def count_none(value):
    return value.filter(poster__isnull=True).count()
