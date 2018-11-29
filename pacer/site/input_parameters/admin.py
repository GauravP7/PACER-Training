from input_parameters.models import SearchCriteria
from django.contrib import admin

class PollAdmin(admin.ModelAdmin):
    list_display = ('search_criteria_id','case_number','case_status', 'from_field_date', 'to_field_date', 'from_last_entry_date', 'to_last_entry_date', 'nature_of_suit', 'cause_of_action', 'last_name', 'first_name', 'middle_name', 'type', 'exact_matches_only', )

admin.site.register(SearchCriteria, PollAdmin)
