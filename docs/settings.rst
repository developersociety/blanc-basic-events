========
Settings
========


EVENTS_CALENDAR_NAME
====================

Default: ``'Events'``

The name of the calendar used for the iCal feed. You'll probably want to
replace this with the name of the site.

EVENTS_CALENDAR_DESCRIPTION
===========================

Default: ``'Events Calendar'``

The long description for the name of the calendar.

EVENTS_START_SUNDAY
===================

Default: ``True``

For recurring events, this will change the choices for the day of the week
field. The default is ``True`` - making Sunday the start of the week. Setting
this to ``False`` will make Monday the start of the week.

.. note::

    Changing this value after deployment will not change any existing data.
    Sunday at the start of the week is stored as ``0``, and Sunday at the end
    of the week is stored as ``7``.

    Your database will need updating after changing this value.
