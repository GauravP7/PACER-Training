from input_parameters.models import Extractor
from input_parameters.models import ExtractorType
from django.contrib import admin
from django.contrib import auth
from django.contrib.sites.models import Site
from django import forms

class ExtractorDisplay(admin.ModelAdmin):
    list_display = ('id', 'get_extractor_type_value', 'case_number','case_status',
                    'from_field_date', 'to_field_date', 'from_last_entry_date', 'to_last_entry_date',
                    'nature_of_suit', 'cause_of_action', 'last_name',
                    'first_name', 'middle_name', 'type', 'exact_matches_only',)
    def get_extractor_type_value(self, obj):
        return obj.extractor_type.extractor_type_value

    get_extractor_type_value.short_description = 'Courtcase type Value'

class ExtractorTypeDisplay(admin.ModelAdmin):
    list_display = ('id','extractor_type_value',)

    def __unicode__(self):
        return self.extractor_type.extractor_type_value

admin.site.register(Extractor, ExtractorDisplay)
admin.site.register(ExtractorType, ExtractorTypeDisplay)
admin.site.unregister(Site)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
