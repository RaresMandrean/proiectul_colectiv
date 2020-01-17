from django import template
from django.contrib.auth.models import Group
from django.conf import settings


register = template.Library()


@register.filter(name='is_approved_organiser')
def is_approved_organiser(user):
    try:
        group = Group.objects.get(name=settings.APPROVED_ORGANISERS)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()


@register.filter(name='is_rejected_organiser')
def is_rejected_organiser(user):
    try:
        group = Group.objects.get(name=settings.REJECTED_ORGANISERS)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()
