from django.contrib import admin
from .models import Category, Event, RecurringEvent, RecurringEventExclusion


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {
       'slug': ('title',)
    }


class RecurringEventInline(admin.TabularInline):
    model = RecurringEvent
    extra = 1


class RecurringEventExclusionInline(admin.TabularInline):
    model = RecurringEventExclusion
    extra = 0


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {
       'slug': ('title',)
    }
    inlines = [
        RecurringEventInline,
        RecurringEventExclusionInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
