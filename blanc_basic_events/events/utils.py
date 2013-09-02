from django.utils import timezone
from blanc_basic_events.events.models import Event
from dateutil import rrule
from dateutil.relativedelta import relativedelta


def sorted_event_list(start_date=None, end_date=None, queryset=None, limit=None):
    # Default start date
    if start_date is None:
        start_date = timezone.now()

    # Default end date
    if end_date is None:
        end_date = start_date + relativedelta(months=+1)

    # Need matching naive versions
    current_zone = timezone.get_default_timezone()
    start_date_naive = timezone.make_naive(start_date, current_zone)
    end_date_naive = timezone.make_naive(end_date, current_zone)

    event_list = []

    if queryset is None:
        event_queryset = Event.objects.all()
    else:
        event_queryset = queryset

    for event in event_queryset.prefetch_related('recurringevent_set', 'recurringeventexclusion_set'):
        if event.recurringevent_set.all():
            # Recurring event
            for i in event.recurringevent_set.all():
                event_ruleset = rrule.rruleset()
                event_ruleset.rrule(i.rrule())

                # Add in any exclusions
                for j in event.recurringeventexclusion_set.all():
                    event_ruleset.exdate(timezone.make_naive(j.date, current_zone))

                # Only add dates in the month we're viewing
                for j in event_ruleset.between(start_date_naive, end_date_naive):
                    event_occurance_tz = timezone.make_aware(j, current_zone)
                    event_list.append((event_occurance_tz, event))
        else:
            # One off event
            if end_date > event.start > start_date:
                event_list.append((event.start, event))

    # Sort by date
    event_list.sort(key=lambda x: x[0])

    # Limited number of events
    if limit is not None:
        event_list = event_list[:limit]

    return event_list
