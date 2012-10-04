from django import template
from blanc_basic_events.events.models import Event

register = template.Library()


@register.assignment_tag
def get_events():
    return Event.objects.all().prefetch_related('recurringevent_set', 'recurringeventexclusion_set')
