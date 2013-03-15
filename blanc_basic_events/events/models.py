from django.db import models
from django.utils import timezone
from dateutil import rrule


DAY_CHOICES = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

FREQUENCY_CHOICES = (
    (91, 'Daily'),
    (1, 'Weekly'),
    (4, 'Monthly'),
    (11, 'Monthly - First'),
    (12, 'Monthly - Second'),
    (13, 'Monthly - Third'),
    (14, 'Monthly - Fourth'),
    (15, 'Monthly - Fifth'),
    (19, 'Monthly - Last'),
)


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blanc_basic_events:category-event-list', (), {
            'slug': self.slug,
        })


class Event(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(
           upload_to='events',
           blank=True, null=True,
           height_field='image_height', width_field='image_width')
    image_height = models.PositiveIntegerField(editable=False, null=True)
    image_width = models.PositiveIntegerField(editable=False, null=True)
    summary = models.CharField(
            max_length=100,
            help_text='A short sentence description of the event.')
    description = models.TextField(help_text='All of the event details we have.')

    start = models.DateTimeField(
            help_text='Start time/date.')
    end = models.DateTimeField(
            help_text='End time/date.')
    final_date = models.DateTimeField(editable=False, null=True, db_index=True)

    class Meta:
        ordering = ('start',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        current_zone = timezone.get_default_timezone()

        # Set final date to the end, for one off events
        self.final_date = self.end

        # But find the last recurring event if possible
        if self.recurringevent_set.all():
            last_date = None

            # Recurring, find the last date
            for i in self.recurringevent_set.all():
                event_ruleset = rrule.rruleset()
                event_ruleset.rrule(i.rrule())

                # Add in any exclusions
                for j in self.recurringeventexclusion_set.all():
                    event_ruleset.exdate(timezone.make_naive(j.date, current_zone))

                try:
                    last_recurring_date = event_ruleset[-1]

                    if last_date is None or last_recurring_date > last_date:
                        last_date = last_recurring_date
                except IndexError:
                    pass

            if last_date:
                self.final_date = timezone.make_aware(last_date, current_zone)

        super(Event, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('blanc_basic_events:event-detail', (), {
            'slug': self.slug,
        })


class RecurringEvent(models.Model):
    event = models.ForeignKey(Event)
    meeting_frequency = models.PositiveIntegerField(choices=FREQUENCY_CHOICES)
    recurring_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('recurring_until',)

    def __unicode__(self):
        return unicode(self.recurring_until)

    def rrule(self):
        # Find the day of the week, needed for monthly events
        weekday = self.event.start.weekday()
        day = rrule.weekdays[weekday]

        # Default = weekly
        interval = 1
        freq = rrule.WEEKLY

        # Daily
        if self.meeting_frequency == 91:
            freq = rrule.DAILY

        # Fortnightly (weekly, interval = 2)
        if self.meeting_frequency == 2:
            interval = 2

        # Monthly (interval = 1)
        if self.meeting_frequency in (4, 11, 12, 13, 14, 15, 19):
            freq = rrule.MONTHLY

        rrule_kwargs = {}

        # And other weird things have offsets
        if self.meeting_frequency in (11, 12, 13, 14, 15, 19):
            if self.meeting_frequency == 11:
                offset = 1
            elif self.meeting_frequency == 12:
                offset = 2
            elif self.meeting_frequency == 13:
                offset = 3
            elif self.meeting_frequency == 14:
                offset = 4
            elif self.meeting_frequency == 15:
                offset = 5
            elif self.meeting_frequency == 19:
                offset = -1

            rrule_kwargs['byweekday'] = day(offset)

        default_timezone = timezone.get_default_timezone()

        # Last recurring date
        rrule_kwargs['until'] = timezone.make_naive(self.recurring_until, default_timezone)

        naive_start = timezone.make_naive(self.event.start, default_timezone)
        return rrule.rrule(freq, interval=interval, dtstart=naive_start, **rrule_kwargs)


class RecurringEventExclusion(models.Model):
    event = models.ForeignKey(Event)
    date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return unicode(self.date)
