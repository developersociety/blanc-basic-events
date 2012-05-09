from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    # iCal feed
    url(r'^events.ics',
        views.ical_feed,
        name='feed'),

    # Pages
    url(r'^special/$',
        views.SpecialEventListView.as_view(),
        name='special-list'),
    url(r'^regular/$',
        views.RegularEventListView.as_view(),
        name='regular-list'),
)
