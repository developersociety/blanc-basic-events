from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from blanc_basic_assets.fields import AssetForeignKey


EVENTS_START_SUNDAY = getattr(settings, 'EVENTS_START_SUNDAY', True)


@python_2_unicode_compatible
class SpecialEvent(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = AssetForeignKey('assets.Image', null=True, blank=True)
    summary = models.CharField(
        max_length=100, help_text='A short sentence description of the event')
    description = models.TextField(help_text='All of the event details we have')
    start = models.DateTimeField(help_text='Start time/date.', db_index=True)
    start_date = models.DateField(editable=False, db_index=True)
    end = models.DateTimeField(help_text='End time/date.')
    end_date = models.DateField(editable=False, db_index=True)
    published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('start',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Used for easy queryset filtering
        self.start_date = self.start.date()
        self.end_date = self.end.date()

        super(SpecialEvent, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blanc_basic_events:specialevent-detail', kwargs={
            'slug': self.slug,
        })

    def clean(self):
        if self.start and self.end and self.start > self.end:
            raise ValidationError('Start date must be earlier than end date.')


@python_2_unicode_compatible
class RecurringEvent(models.Model):
    DAY_CHOICES = (
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    day_of_the_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES, db_index=True)
    time = models.TimeField(db_index=True)
    frequency = models.CharField(max_length=200, blank=True)
    published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('day_of_the_week', 'time')

    def __str__(self):
        return self.title
