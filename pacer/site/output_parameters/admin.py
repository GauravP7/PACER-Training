from output_parameters.models import PageContent
from output_parameters.models import CaseDetails
from output_parameters.models import AdditionalInfo
from django.contrib import admin

class PageContentDisplay(admin.ModelAdmin):
    list_display = ('page_content_id', 'page_path',)

class CaseDetailsDisplay(admin.ModelAdmin):
    list_display = ('case_id', 'page_content', 'case_number', 'parties_involved', 'case_filed_date', 'case_closed_date',)

class AdditionalInfoDisplay(admin.ModelAdmin):
    list_display = ('info_id', 'additional_info_json',)

admin.site.register(PageContent, PageContentDisplay)

admin.site.register(CaseDetails, CaseDetailsDisplay)

admin.site.register(AdditionalInfo, AdditionalInfoDisplay)
