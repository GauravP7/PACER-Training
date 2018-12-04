from output_parameters.models import PageContent
from output_parameters.models import CaseDetails
from output_parameters.models import AdditionalInfo
from output_parameters.models import PageSourcePath
from django.contrib import admin

class PageContentDisplay(admin.ModelAdmin):
    list_display = ('id', 'page_path',)

class CaseDetailsDisplay(admin.ModelAdmin):
    list_display = ('id','pacer_case_id','case_number', 'parties_involved', 'case_filed_date', 'case_closed_date',)

class AdditionalInfoDisplay(admin.ModelAdmin):
    list_display = ('id', 'additional_info_json',)

class PageSourcePathDisplay(admin.ModelAdmin):
    list_display = ('id', 'page_value_json',)

admin.site.register(PageContent, PageContentDisplay)

admin.site.register(CaseDetails, CaseDetailsDisplay)

admin.site.register(PageSourcePath, PageSourcePathDisplay)

admin.site.register(AdditionalInfo, AdditionalInfoDisplay)
