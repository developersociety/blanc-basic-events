========
Overview
========


What is blanc-basic-events?
===========================

blanc-basic-events is a simple Django package to manage a list of recurring
events and special events to be displayed on a site.


Design notes
============

Two different types of events
-----------------------------

The events package has split events into two types - recurring events and
special events. This is intentionally done to keep events as simple as
possible.

Recurring events
----------------

Recurring events are typically weekly events which occur on a regular basis.
You can pick the day of the week the event occurs on, and how frequently it
occurs is up to you to describe as text - instead of being limited to a small
number of options which might not describe when it occurs.

These events are only listed on the recurring events list page.

Special events
--------------

Special events are one-off events, although they may happen again at a future
date - you'll have to add it again. This is intended for events of importance
which may be promoted elsewhere on the site.

These events are listed on the events list page, and also get a page for each
event.
