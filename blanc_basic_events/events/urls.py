from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    # Event list/detail
    url(r'^$',
        views.EventListView.as_view(),
        name='event-list'),
    url(r'^category/(?P<slug>[-\w]+)/$',
        views.CategoryEventListView.as_view(),
        name='category-event-list'),
    url(r'^view/(?P<slug>[-\w]+)/$',
        views.EventDetailView.as_view(),
        name='event-detail'),

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
