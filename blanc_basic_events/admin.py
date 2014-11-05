from django.contrib import admin
from .models import SpecialEvent, RecurringEvent


@admin.register(SpecialEvent)
class SpecialEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'published')
    list_filter = ('start', 'published')
    ordering = ('-start',)
    date_hierarchy = 'start'
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'day_of_the_week', 'time', 'published')
    list_filter = ('day_of_the_week', 'published')
