from output_parameters.models import DownloadTracker
from output_parameters.models import Courtcase
from output_parameters.models import AdditionalInfo
from output_parameters.models import CourtcaseSource
from output_parameters.models import CourtcaseSourceDataPath
from django.contrib import admin

class DownloadTrackerDisplay(admin.ModelAdmin):
    list_display = ('id', 'page_path',)

class CourtcaseDisplay(admin.ModelAdmin):
    list_display = ('id', 'pacer_case_id', 'case_number', 'parties_involved', 'case_filed_date', 'case_closed_date',)

class CourtcaseSourceDisplay(admin.ModelAdmin):
    list_display = ('id', 'value',)

class AdditionalInfoDisplay(admin.ModelAdmin):
    list_display = ('id', 'additional_info_json',)

class CourtcaseSourceDataPathDisplay(admin.ModelAdmin):
    list_display = ('id', 'page_value_json',)

admin.site.register(DownloadTracker, DownloadTrackerDisplay)

admin.site.register(Courtcase, CourtcaseDisplay)

admin.site.register(CourtcaseSource, CourtcaseSourceDisplay)

admin.site.register(CourtcaseSourceDataPath, CourtcaseSourceDataPathDisplay)

admin.site.register(AdditionalInfo, AdditionalInfoDisplay)
