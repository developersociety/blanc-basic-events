from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


default_app_config = 'blanc_basic_events.apps.BlancBasicEventsConfig'


def get_special_events_model():
    try:
        conf_model = getattr(settings, 'EVENTS_SPECIAL_MODEL', 'events.SpecialEvent')
        return django_apps.get_model(conf_model)
    except ValueError:
        raise ImproperlyConfigured("EVENTS_SPECIAL_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured("EVENTS_SPECIAL_MODEL refers to model '%s' that has not been installed" % conf_model)


def get_recurring_events_model():
    try:
        conf_model = getattr(settings, 'EVENTS_RECURRING_MODEL', 'events.RecurringEvent')
        return django_apps.get_model(conf_model)
    except ValueError:
        raise ImproperlyConfigured("EVENTS_RECURRING_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured("EVENTS_RECURRING_MODEL refers to model '%s' that has not been installed" % conf_model)
