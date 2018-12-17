# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class ExtractorType(models.Model):
    id = models.AutoField(primary_key=True)
    extractor_type_value = models.CharField(max_length=165, blank=True)
    class Meta:
        db_table = u'extractor_type'

class Extractor(models.Model):
    id = models.AutoField(primary_key=True)
    extractor_type = models.ForeignKey(ExtractorType, null=True, blank=True)
    is_local_parsing = models.IntegerField(null=True, blank=True)
    pacer_case_id = models.CharField(max_length=165, blank=True)
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
        db_table = u'extractor'

class DownloadTracker(models.Model):
    id = models.AutoField(primary_key=True)
    is_parsed = models.IntegerField(null=True, blank=True)
    page_path = models.CharField(max_length=330, blank=True)
    class Meta:
        db_table = u'download_tracker'


class CourtcaseSource(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=165, blank=True)
    class Meta:
        db_table = u'courtcase_source'

class Courtcase(models.Model):
    id = models.AutoField(primary_key=True)
    download_tracker = models.ForeignKey(DownloadTracker)
    courtcase_source_value = models.ForeignKey(CourtcaseSource, db_column='courtcase_source_value')
    pacer_case_id = models.CharField(max_length=165, unique=True, blank=True)
    case_number = models.CharField(max_length=165, unique=True, blank=True)
    parties_involved = models.CharField(max_length=765, blank=True)
    case_filed_date = models.DateField(null=True, blank=True)
    case_closed_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'courtcase'

class CourtcaseSourceDataPath(models.Model):
    id = models.AutoField(primary_key=True)
    courtcase = models.ForeignKey(Courtcase, null=True, blank=True)
    page_value_json = models.TextField(blank=True)
    class Meta:
        db_table = u'courtcase_source_data_path'

class AdditionalInfo(models.Model):
    id = models.AutoField(primary_key=True)
    courtcase = models.ForeignKey(Courtcase, null=True, blank=True)
    additional_info_json = models.TextField(blank=True)
    class Meta:
        db_table = u'additional_info'
