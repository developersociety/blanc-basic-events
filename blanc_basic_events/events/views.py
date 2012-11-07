from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView
from .models import Category, Event
from django.contrib.sites.models import Site, RequestSite
from django.contrib.syndication.views import add_domain
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from dateutil import rrule
import vobject


class EventListView(ListView):
    model = Event

    def get_queryset(self):
        return self.model.objects.filter(final_date__gte=timezone.now())


class CategoryEventListView(ListView):
    model = Event
    template_name_suffix = '_bycategory_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.model.objects.filter(final_date__gte=timezone.now(), category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryEventListView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class EventDetailView(DetailView):
    model = Event


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

    # Events
    for event in Event.objects.all().prefetch_related('recurringevent_set', 'recurringeventexclusion_set'):
        if event.recurringevent_set.all():
            # Recurring event
            for i in event.recurringevent_set.all():
                v = cal.add('vevent')

                v.add('uid').value = 'recurring-event-%d@%s' % (i.id, current_site)
                v.add('summary').value = event.title

                v.add('dtstart').value = event.start
                v.add('dtend').value = event.end

                event_ruleset = rrule.rruleset()
                event_ruleset.rrule(i.rrule())

                # Add in any exclusions
                for j in event.recurringeventexclusion_set.all():
                    event_ruleset.exdate(j.date)

                v.rruleset = event_ruleset
        else:
            # One off event
            v = cal.add('vevent')

            v.add('uid').value = 'event-%d@%s' % (event.id, current_site)
            v.add('summary').value = event.title

            v.add('dtstart').value = event.start
            v.add('dtend').value = event.end

    icalstream = cal.serialize()

    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Filename'] = 'events.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=events.ics'

    return response


def calendar_index(request):
    date_now = timezone.now()
    return calendar_month(request, date_now.year, date_now.month)


def calendar_month(request, year, month):
    year = int(year)
    month = int(month)

    # Ensure we have a valid month
    try:
        view_month = datetime.datetime(year, month, 1)
        view_month_end = view_month + relativedelta(months=+1, seconds=-1)
    except ValueError:
        raise Http404

    # Don't allow infinite years
    date_now = datetime.datetime.now()
    if view_month.year > date_now.year + getattr(settings, 'EVENTS_YEAR_MAX', 1) or view_month.year < date_now.year - getattr(settings, 'EVENTS_YEAR_MIN', 1):
        raise Http404

    # Need matching timezone aware versions
    current_zone = timezone.get_default_timezone()
    view_month_tz = timezone.make_aware(view_month, current_zone)
    view_month_end_tz = timezone.make_aware(view_month_end, current_zone)

    event_list = []

    for event in Event.objects.all().prefetch_related('recurringevent_set', 'recurringeventexclusion_set'):
        if event.recurringevent_set.all():
            # Recurring event
            for i in event.recurringevent_set.all():
                event_ruleset = rrule.rruleset()
                event_ruleset.rrule(i.rrule())

                # Add in any exclusions
                for j in event.recurringeventexclusion_set.all():
                    event_ruleset.exdate(timezone.make_naive(j.date, current_zone))

                # Only add dates in the month we're viewing
                for j in event_ruleset.between(view_month, view_month_end):
                    event_occurance_tz = timezone.make_aware(j, current_zone)
                    event_list.append((event_occurance_tz, event))
        else:
            # One off event
            if view_month_end_tz > event.start > view_month_tz:
                event_list.append((event.start, event))

    # Sort by date
    event_list.sort(key=lambda x: x[0])

    # Navigation prev/next month
    previous_month = view_month + relativedelta(months=-1)
    next_month = view_month + relativedelta(months=1)

    if previous_month.year < date_now.year - getattr(settings, 'EVENTS_YEAR_MIN', 1):
        previous_month = None

    if next_month.year > date_now.year + getattr(settings, 'EVENTS_YEAR_MAX', 1):
        next_month = None

    return TemplateResponse(request, 'events/calendar_month.html', {
        'event_list': event_list,
        'previous_month': previous_month,
        'next_month': next_month,
    })
