from my_app.models import AdditionalInfo
from my_app.models import CaseDetails
from my_app.models import PageContent
from my_app.models import SearchCriteria
from django.contrib import admin

class MysiteAdmin(admin.ModelAdmin):
    fields = ['page_content_id', 'page_path']
admin.site.register(AdditionalInfo)
#admin.site.register(CaseDetails)
#admin.site.register(PageContent)
#admin.site.register(SearchCriteria)
