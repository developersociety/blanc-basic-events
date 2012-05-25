from django import template
from blanc_basic_events.events.models import RegularEvent, SpecialEvent

register = template.Library()


@register.assignment_tag
def get_regular_events():
    return RegularEvent.objects.all()


@register.assignment_tag
def get_special_events():
    return SpecialEvent.objects.all()
