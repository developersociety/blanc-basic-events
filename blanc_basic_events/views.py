import datetime

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from icalendar import Calendar, Event

from .models import RecurringEvent, SpecialEvent


class EventsHomeView(ListView):
    queryset = RecurringEvent.objects.filter(published=True)
    allow_empty = True

    def special_events_this_week(self):
        today = datetime.date.today()
        next_week = today + datetime.timedelta(days=7)
        return SpecialEvent.objects.filter(
            end_date__gte=today, start_date__lte=next_week, published=True)

    def upcoming_special_events(self):
        return SpecialEvent.objects.filter(
            end_date__gte=datetime.date.today(), published=True)


class SpecialEventListView(ListView):
    model = SpecialEvent

    def get_queryset(self):
        return self.model.objects.filter(published=True, end_date__gte=datetime.date.today())


class SpecialEventDetailView(DetailView):
    queryset = SpecialEvent.objects.filter(published=True)


# iCal feed
def ical_feed(request):
    cal = Calendar()

    cal.add('prodid', '-//Events Calendar//blanc-basic-events//EN')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', getattr(settings, 'EVENTS_CALENDAR_NAME', 'Events'))
    cal.add('x-wr-caldesc', getattr(settings, 'EVENTS_CALENDAR_DESCRIPTION', 'Events Calendar'))

    domain = get_current_site(request).domain

    # Events
    today = datetime.date.today()
    for i in SpecialEvent.objects.filter(published=True, end_date__gte=today):
        event = Event(uid='%d@%s' % (i.id, domain), summary=i.title)
        event.add('dtstart', i.start)  # Ensure the datetime gets encoded
        event.add('dtend', i.end)
        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=events.ics'

    return response
