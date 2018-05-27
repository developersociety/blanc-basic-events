============
Installation
============

Requirements
============

Before installing blanc-basic-events, you'll need a copy of Django__ 1.7,
and blanc-basic-assets__ installed.

.. __: http://www.djangoproject.com/
.. __: https://github.com/developersociety/blanc-basic-assets


Installing blanc-basic-events
=============================

The fastest way of installing is to use pip__.

.. __: http://www.pip-installer.org/

Simply type::

    pip install blanc-basic-events

Manual installation
-------------------

Alternative you manually install by downloading the latest version from the
`blanc-basic-events page on the Python Package Index`__.

.. __: http://pypi.python.org/pypi/blanc-basic-events/

Download the package, unpack it and run the ``setup.py`` installation
script::

    python setup.py install


Configuring your project
========================

Edit your Django project's settings module, ensure that the required
dependencies are installed and configured, then add ``blanc_basic_events`` to
``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'blanc_basic_assets',
        ...
        'blanc_basic_events',
    ]

Also in the settings file you should edit the title for iCal feeds::

    EVENTS_CALENDAR_NAME = "My Site"

Once this is done, run ``python manage.py migrate`` to update your database.

Edit your Django project's URL config file, and add the URL pattern for events::

    urlpatterns = [
        ...

        # Events
        url(r'^events/', include('blanc_basic_events.urls', namespace='blanc_basic_events')),
    ]

Then your project will be ready to use the events package.
