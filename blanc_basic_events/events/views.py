from django.http import HttpResponse
from django.views.generic import ListView
from .models import RegularEvent, SpecialEvent
from django.contrib.sites.models import Site, RequestSite
from django.contrib.syndication.views import add_domain
from django.conf import settings
import datetime
import calendar
from dateutil.relativedelta import *
import vobject


# iCal feed
def ical_feed(request):
    # We need an appropriate hostname
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    # Calendar object with various settings needed
    cal = vobject.iCalendar()

    cal.add('X-WR-TIMEZONE').value = settings.TIME_ZONE
    cal.add('X-WR-CALNAME').value = 'Events'
    cal.add('X-WR-CALDESC').value = 'Events Calendar'
    cal.add('CALSCALE').value = 'GREGORIAN'

    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this

    # Special one off events
    for event in SpecialEvent.objects.all():
        v = cal.add('vevent')

        v.add('uid').value = 'special-event-%d@%s' % (event.id, current_site)
        v.add('summary').value = event.title

        v.add('dtstart').value = event.start
        v.add('dtend').value = event.end

    # Regular events
    for event in RegularEvent.objects.all():
        v = cal.add('vevent')

        v.add('uid').value = 'regular-event-%d@%s' % (event.id, current_site)
        v.add('summary').value = event.title

        v.add('dtstart').value = event.start
        v.add('dtend').value = event.end

        v.rruleset = event.rruleset()

    icalstream = cal.serialize()

    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Filename'] = 'events.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=events.ics'

    return response


class SpecialEventListView(ListView):
    model = SpecialEvent


class RegularEventListView(ListView):
    model = RegularEvent
