# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import blanc_basic_assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringEvent',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('description', models.TextField()),
                ('day_of_the_week', models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('time', models.TimeField(db_index=True)),
                ('frequency', models.CharField(max_length=200, blank=True)),
                ('published', models.BooleanField(default=True, db_index=True)),
            ],
            options={
                'ordering': ('day_of_the_week', 'time'),
            },
        ),
        migrations.CreateModel(
            name='SpecialEvent',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('summary', models.CharField(max_length=100, help_text='A short sentence description of the event')),
                ('description', models.TextField(help_text='All of the event details we have')),
                ('start', models.DateTimeField(help_text='Start time/date.', db_index=True)),
                ('start_date', models.DateField(editable=False, db_index=True)),
                ('end', models.DateTimeField(help_text='End time/date.')),
                ('end_date', models.DateField(editable=False, db_index=True)),
                ('published', models.BooleanField(default=True, db_index=True)),
                ('image', blanc_basic_assets.fields.AssetForeignKey(blank=True, null=True, to='assets.Image')),
            ],
            options={
                'ordering': ('start',),
            },
        ),
    ]
