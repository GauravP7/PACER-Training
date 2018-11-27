# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class PageContent(models.Model):
    page_content_id = models.IntegerField(primary_key=True)
    page_path = models.CharField(max_length=330, blank=True)
    class Meta:
        db_table = u'page_content'

class CaseDetails(models.Model):
    case_id = models.IntegerField(primary_key=True)
    page_content = models.ForeignKey(PageContent)
    case_number = models.CharField(max_length=165, blank=True)
    parties_involved = models.CharField(max_length=765, blank=True)
    case_filed_date = models.DateField(null=True, blank=True)
    case_closed_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'case_details'

class AdditionalInfo(models.Model):
    info_id = models.IntegerField(primary_key=True)
    case = models.ForeignKey(CaseDetails, null=True, blank=True)
    additional_info_json = models.TextField(blank=True)
    class Meta:
        db_table = u'additional_info'

class SearchCriteria(models.Model):
    search_criteria_id = models.IntegerField(primary_key=True)
    case_number = models.CharField(max_length=165, blank=True)
    case_status = models.CharField(max_length=165, blank=True)
    from_field_date = models.DateField(null=True, blank=True)
    to_field_date = models.DateField(null=True, blank=True)
    from_last_entry_date = models.DateField(null=True, blank=True)
    to_last_entry_date = models.DateField(null=True, blank=True)
    nature_of_suit = models.CharField(max_length=165, blank=True)
    cause_of_action = models.CharField(max_length=165, blank=True)
    last_name = models.CharField(max_length=165, blank=True)
    first_name = models.CharField(max_length=165, blank=True)
    middle_name = models.CharField(max_length=165, blank=True)
    type = models.CharField(max_length=165, blank=True)
    exact_matches_only = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'search_criteria'
