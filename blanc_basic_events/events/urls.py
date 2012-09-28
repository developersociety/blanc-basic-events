from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    # iCal feed
    url(r'^events.ics',
        views.ical_feed,
        name='feed'),
)
