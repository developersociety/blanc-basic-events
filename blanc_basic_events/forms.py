from django import forms
from django.conf import settings

from .models import RecurringEvent


EVENTS_START_SUNDAY = getattr(settings, 'EVENTS_START_SUNDAY', True)


class BaseRecurringEventAdminForm(forms.ModelForm):
    class Meta:
        model = RecurringEvent
        exclude = ()


def recurringevent_admin_form():
    start_week = ((0, 'Sunday'),) if EVENTS_START_SUNDAY else ()
    end_week = ((7, 'Sunday'),) if not EVENTS_START_SUNDAY else ()
    day_choices = start_week + (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ) + end_week

    class RecurringEventAdminForm(BaseRecurringEventAdminForm):
        day_of_the_week = forms.ChoiceField(choices=day_choices)

    return RecurringEventAdminForm
