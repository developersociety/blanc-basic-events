from django.db.models.signals import post_save, post_delete
from .models import Event, RecurringEvent, RecurringEventExclusion


def update_event(sender, instance, raw=False, **kwargs):
    if not raw:
        try:
            instance.event.save()
        except Event.DoesNotExist:
            pass


post_save.connect(update_event, sender=RecurringEvent)
post_save.connect(update_event, sender=RecurringEventExclusion)
post_delete.connect(update_event, sender=RecurringEvent)
post_delete.connect(update_event, sender=RecurringEventExclusion)
