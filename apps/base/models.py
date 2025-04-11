from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
# from .models_extended import *


# AUTOGEN_BEGIN_ChartField#
class ChartField(BaseModel):
    chart_field_id      = models.CharField(max_length=  7, blank=False, unique=False, primary_key=True )
    hotel               = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, default='001')
    code                = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False, default='')
    description         = models.CharField(max_length=254, blank=False, unique=False, primary_key=False)
    description_short   = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='021')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_chart_field'
        verbose_name_plural = 'Chart Fields (base_chart_field)'
        ordering            = []
        
    def __str__(self):
        return 'chart_field'
# AUTOGEN_END_ChartField#


# AUTOGEN_BEGIN_Company#
class Company(BaseModel):
    company_id          = models.CharField(max_length=  5, blank=False, unique=True , primary_key=True )
    client              = models.ForeignKey("static.Client", on_delete=models.CASCADE, related_name='+', default='000')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, default='001')
    code                = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False, default='')
    description         = models.CharField(max_length= 70, blank=False, unique=False, primary_key=False, default='')
    description_short   = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False, default='')
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='021')
    grouping            = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    company_key         = models.CharField(max_length= 70, blank=False, unique=False, primary_key=False, default='')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_company'
        verbose_name_plural = 'companies (base_company)'
        ordering            = []
        
    def __str__(self):
        return 'company'
# AUTOGEN_END_Company#


# AUTOGEN_BEGIN_ExternalMapping#
class ExternalMapping(BaseModel):
    external_mapping_id = models.CharField(max_length=  9, blank=False, unique=True , primary_key=True )
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='999')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    app_name            = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False, default='')
    model_name          = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False, default='')
    external_id         = models.CharField(max_length= 50, blank=False, unique=True , primary_key=False, default='')
    internal_id         = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False, default='')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_external_mapping'
        verbose_name_plural = 'mappings (base_external_mapping)'
        ordering            = []
        
    def __str__(self):
        return 'external_mapping'
# AUTOGEN_END_ExternalMapping#


# AUTOGEN_BEGIN_Identifier#
class Identifier(models.Model):
    identifier_id    = models.CharField(max_length= 40, blank=False, unique=True , primary_key=True )
    last_identifier  = models.IntegerField(default=0)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_identifier'
        verbose_name_plural = 'identifiers (base_identifier)'
        ordering            = []
        
    def __str__(self):
        return 'identifier'
# AUTOGEN_END_Identifier#


# AUTOGEN_BEGIN_Person#
class Person(BaseModel):
    person_id        = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    client           = models.ForeignKey("static.Client", on_delete=models.CASCADE, related_name='+', default='999')
    grouping         = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False, default='')
    order_by         = models.CharField(max_length=  2, blank=True , unique=False, primary_key=False, default='99')
    code             = models.CharField(max_length= 15, blank=True , unique=False, primary_key=False)
    first_name       = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    middle_name      = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    last_name        = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    birth_date       = models.DateTimeField(default=beginning_of_time)
    email            = models.TextField(blank=True , unique=False, primary_key=False, default='')
    gender_type      = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='700')
    person_key       = models.CharField(max_length= 50, blank=True , unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_person'
        verbose_name_plural = 'people (base_person)'
        ordering            = []
        
    def __str__(self):
        return self.last_name+', '+self.first_name
# AUTOGEN_END_Person#


# AUTOGEN_BEGIN_User#
class User(AbstractUser, BaseModel):
    user_id             = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    access_user_id      = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False, default='')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, default='041')
    person              = models.ForeignKey("base.Person", on_delete=models.CASCADE, default='A9999')
    grouping            = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False, default='')
    code                = models.CharField(max_length= 10, blank=True , unique=False, primary_key=False)
    description         = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    # username            = models.CharField(max_length=150, blank=True , unique=False, primary_key=False)
    # password            = models.CharField(max_length=100, blank=True , unique=False, primary_key=False, null=True)
    # is_staff            = models.BooleanField(default=True)
    # is_active           = models.BooleanField(default=True)
    # is_superuser        = models.BooleanField(default=False)
    user_key            = models.CharField(max_length= 50, blank=True , unique=False, primary_key=False, default='')
    start_date          = models.DateTimeField(default=today)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", db_column="effective_status_id", default='021')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    external_id         = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False)
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_user'
        verbose_name_plural = 'users (base_user)'
        ordering            = []
        
    def __str__(self):
        return self.code + ' ' + self.description
# AUTOGEN_END_User#


