from django.contrib import admin
from django.contrib.sites.models import Site
from .models import RegularEvent, RegularEventExclusion, SpecialEvent


class RegularEventExclusionInline(admin.TabularInline):
    model = RegularEventExclusion
    extra = 1


class RegularEventAdmin(admin.ModelAdmin):
    inlines = [RegularEventExclusionInline]


admin.site.register(RegularEvent, RegularEventAdmin)
admin.site.register(SpecialEvent)
