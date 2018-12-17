from output_parameters.models import DownloadTracker
from output_parameters.models import Courtcase
from output_parameters.models import AdditionalInfo
from output_parameters.models import CourtcaseSource
from output_parameters.models import CourtcaseSourceDataPath
from django.contrib import admin

class DownloadTrackerDisplay(admin.ModelAdmin):
    list_display = ('id', 'is_parsed', 'page_path',)

class CourtcaseDisplay(admin.ModelAdmin):
    list_display = ('id', 'get_courtcase_source_value', 'pacer_case_id', 'case_number', 'parties_involved', 'case_filed_date', 'case_closed_date',)

    search_fields = ['case_number']

    def get_courtcase_source_value(self, obj):
        return obj.courtcase_source_value.value

    get_courtcase_source_value.short_description = 'Courtcase Source Value'

class CourtcaseSourceDisplay(admin.ModelAdmin):
    list_display = ('id', 'value',)

class AdditionalInfoDisplay(admin.ModelAdmin):
    list_display = ('id', 'courtcase_id', 'additional_info_json',)

    def courtcase_id(self, obj):
        return obj.courtcase_id

class CourtcaseSourceDataPathDisplay(admin.ModelAdmin):
    list_display = ('id', 'get_courtcase_id', 'page_value_json',)

    def get_courtcase_id(self, obj):
        return obj.courtcase.id

    get_courtcase_id.short_description = 'Courtcase ID'

admin.site.register(DownloadTracker, DownloadTrackerDisplay)

admin.site.register(Courtcase, CourtcaseDisplay)

admin.site.register(CourtcaseSource, CourtcaseSourceDisplay)

admin.site.register(CourtcaseSourceDataPath, CourtcaseSourceDataPathDisplay)

admin.site.register(AdditionalInfo, AdditionalInfoDisplay)
