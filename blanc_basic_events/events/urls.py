from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    # iCal feed
    url(r'^events.ics',
        views.ical_feed,
        name='feed'),

    # Calendar
    url(r'^calendar/$',
        views.calendar_index,
        name='calendar-index'),
    url(r'^calendar/(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.calendar_month,
        name='calendar-month'),
)
