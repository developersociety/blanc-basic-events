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
    (1, 'Weekly'),
    (4, 'Monthly'),
    (11, 'Monthly - First'),
    (12, 'Monthly - Second'),
    (13, 'Monthly - Third'),
    (14, 'Monthly - Fourth'),
    (19, 'Monthly - Last'),
)

class RegularEvent(models.Model):
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
            help_text='First date this will appear in the calendar.')
    end = models.DateTimeField(
            help_text='Last date this will appear in the calendar.')

    meeting_day = models.PositiveIntegerField(
            choices=DAY_CHOICES, editable=False)
    meeting_frequency = models.PositiveIntegerField(choices=FREQUENCY_CHOICES)

    class Meta:
        ordering = ('meeting_day',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.meeting_day = self.start.weekday()
        super(RegularEvent, self).save(*args, **kwargs)

    def rruleset(self):
        # Default = weekly
        interval = 1
        freq = rrule.WEEKLY

        # Fortnightly (weekly, interval = 2)
        if self.meeting_frequency == 2:
            interval = 2

        # Monthly (interval = 1)
        if self.meeting_frequency in ('4', '11', '12', '13', '14', '19'):
            freq = rrule.MONTHLY

        rrule_kwargs = {}

        # Use this by default if there's a day given
        day = rrule.weekdays[self.meeting_day]
        if day:
            rrule_kwargs['byweekday'] = day

        # And other weird things have offsets
        if self.meeting_frequency in ('11', '12', '13', '14', '19'):
            if self.meeting_frequency == '11':
                offset = 1
            elif self.meeting_frequency == '12':
                offset = 2
            elif self.meeting_frequency == '13':
                offset = 3
            elif self.meeting_frequency == '14':
                offset = 4
            elif self.meeting_frequency == '19':
                offset = -1

            rrule_kwargs['byweekday'] = day(offset)

        set = rrule.rruleset()
        set.rrule(rrule.rrule(freq, interval=interval, dtstart=self.start, until=self.end, **rrule_kwargs))

        for i in self.regulareventexclusion_set.all():
            set.exdate(datetime.datetime(i.date.year, i.date.month, i.date.day))

        return set


class RegularEventExclusion(models.Model):
    event = models.ForeignKey(RegularEvent)
    date = models.DateField(db_index=True)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return unicode(self.date)


class SpecialEvent(models.Model):
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
            help_text='First date this will appear in the calendar.')
    end = models.DateTimeField(
            help_text='Last date this will appear in the calendar.')

    class Meta:
        ordering = ('start',)

    def __unicode__(self):
        return self.title
