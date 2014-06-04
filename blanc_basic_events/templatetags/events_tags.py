from django import template
from .. import get_special_events_model
import datetime

register = template.Library()


@register.assignment_tag
def get_upcoming_events(limit=None):
    event_list = get_special_events_model().objects.filter(end_date__gte=datetime.date.today(),
                                                           published=True)

    if limit is None:
        return event_list
    else:
        return event_list[:limit]
