import datetime

from django import template

from ..models import SpecialEvent


register = template.Library()


@register.assignment_tag
def get_upcoming_events(limit=None):
    event_list = SpecialEvent.objects.filter(end_date__gte=datetime.date.today(), published=True)

    if limit is None:
        return event_list
    else:
        return event_list[:limit]
