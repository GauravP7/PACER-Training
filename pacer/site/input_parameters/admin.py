from input_parameters.models import Extractor
from django.contrib import admin
from django.contrib import auth
from django.contrib.sites.models import Site

class ExtractorAdmin(admin.ModelAdmin):
    list_display = ('id','case_number','case_status',
                    'from_field_date', 'to_field_date', 'from_last_entry_date', 'to_last_entry_date',
                    'nature_of_suit', 'cause_of_action', 'last_name',
                    'first_name', 'middle_name', 'type', 'exact_matches_only',
                    )
admin.site.register(Extractor, ExtractorAdmin)
admin.site.unregister(Site)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
