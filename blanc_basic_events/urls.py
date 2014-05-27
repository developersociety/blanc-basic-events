from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    # Event list/detail
    url(r'^$',
        views.EventsHomeView.as_view(),
        name='events-home'),
    url(r'^list/$',
        views.SpecialEventListView.as_view(),
        name='specialevent-list'),
    url(r'^view/(?P<slug>[-\w]+)/$',
        views.SpecialEventDetailView.as_view(),
        name='specialevent-detail'),

    # # iCal feed
    url(r'^events.ics$',
        views.ical_feed,
        name='feed'),
)
