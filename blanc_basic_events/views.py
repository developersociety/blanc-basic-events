from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from icalendar import Calendar, Event
import datetime
from . import get_special_events_model, get_recurring_events_model


class EventsHomeView(ListView):
    queryset = get_recurring_events_model().objects.filter(published=True)
    allow_empty = True

    def special_events_this_week(self):
        today = datetime.date.today()
        next_week = today + datetime.timedelta(days=7)
        return get_special_events_model().objects.filter(end_date__gte=today,
                                                         start_date__lte=next_week,
                                                         published=True)

    def upcoming_special_events(self):
        return get_special_events_model().objects.filter(end_date__gte=datetime.date.today(),
                                                         published=True)


class SpecialEventListView(ListView):
    model = get_special_events_model()

    def get_queryset(self):
        return self.model.objects.filter(published=True, end_date__gte=datetime.date.today())


class SpecialEventDetailView(DetailView):
    queryset = get_special_events_model().objects.filter(published=True)


# iCal feed
def ical_feed(request):
    cal = Calendar()

    cal.add('prodid', '-//Events Calendar//blanc-basic-events//EN')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', getattr(settings, 'EVENTS_CALENDAR_NAME', 'Events'))
    cal.add('x-wr-caldesc', getattr(settings, 'EVENTS_CALENDAR_DESCRIPTION', 'Events Calendar'))

    domain = get_current_site(request).domain

    # Events
    for i in get_special_events_model().objects.filter(published=True, end_date__gte=datetime.date.today()):
        event = Event(uid='%d@%s' % (i.id, domain), summary=i.title)
        event.add('dtstart', i.start)  # Ensure the datetime gets encoded
        event.add('dtend', i.end)
        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=events.ics'

    return response
