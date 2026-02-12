from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
from core.utilities.database_utilties import ModelUtilities as ModelUtil
# from .models_extended import *


# AUTOGEN_BEGIN_Category#
class Category(BaseModel):
    category_id         = models.CharField(max_length=  5, blank=False, unique=True , primary_key=True )
    client              = models.ForeignKey("static.Client", on_delete=models.CASCADE, related_name='+', default='000')
    hotel               = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    parent_category     = models.ForeignKey("self", on_delete=models.CASCADE, to_field='category_id', related_name="+", default=None, null=True)
    order_by            = models.CharField(max_length=  2, blank=False, unique=False, primary_key=False, default='99')
    code                = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False, default='')
    description         = models.CharField(max_length= 90, blank=False, unique=False, primary_key=False)
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='021')
    grouping            = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    category_key        = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False, default='')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_category'
        verbose_name_plural = 'categories (base_category)'
        ordering            = []
        
    def __str__(self):
        return 'category'
# AUTOGEN_END_Category#


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
    external_pk         = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False, default='')
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


# AUTOGEN_BEGIN_HotelType#
class HotelType(BaseModel):
    hotel_type_id    = models.CharField(max_length=  5, blank=False, unique=True , primary_key=True )
    hotel            = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    item             = models.ForeignKey("base.Item", on_delete=models.CASCADE, related_name='+', default='A00000')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_hotel_type'
        verbose_name_plural = 'hotel types (base_hotel_type)'
        ordering            = []
        
    def __str__(self):
        return 'hotel_type'
# AUTOGEN_END_HotelType#


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


# AUTOGEN_BEGIN_Item#
class Item(BaseModel):
    item_id             = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    category            = models.ForeignKey("base.Category", on_delete=models.CASCADE, related_name='+', default='A0000')
    code                = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False, default='')
    description         = models.CharField(max_length= 90, blank=False, unique=False, primary_key=False, default='')
    order_by            = models.CharField(max_length=  2, blank=False, unique=False, primary_key=False, default="99")
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", db_column="effective_status_id", default='021')
    grouping            = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    item_key            = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_item'
        verbose_name_plural = 'items (base_item)'
        ordering            = []
        
    def __str__(self):
        return 'item'
# AUTOGEN_END_Item#


# AUTOGEN_BEGIN_Job#
class Job(BaseModel):
    job_id           = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    order_by         = models.CharField(max_length=  2, blank=False, unique=False, primary_key=False, default='99')
    code             = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    frequency        = models.CharField(max_length=  1, blank=False, unique=False, primary_key=False, default='#', help_text="#=On Demand D=daily H=hourly")
    description      = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    grouping         = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False, default='')
    job_key          = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_job'
        verbose_name_plural = 'job definitions (base_job)'
        ordering            = []
        
    def __str__(self):
        return 'job'
# AUTOGEN_END_Job#


# AUTOGEN_BEGIN_JobRun#
class JobRun(BaseModel):
    job_run_id       = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    job              = models.ForeignKey("base.Job", on_delete=models.CASCADE, related_name="+")
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='041')
    hotel            = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    user             = models.ForeignKey("base.User", on_delete=models.CASCADE, related_name="+", default='A00000', null=True)
    start_date       = models.DateTimeField(default=beginning_of_time)
    end_date         = models.DateTimeField(default=end_of_time)
    record_count     = models.IntegerField(default=-1)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_job_run'
        verbose_name_plural = 'job run (base_job_run)'
        ordering            = []
        
    def __str__(self):
        return 'job_run'
# AUTOGEN_END_JobRun#


# AUTOGEN_BEGIN_Parameter#
class Parameter(BaseModel):
    parameter_id     = models.CharField(max_length=  7, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    user             = models.ForeignKey("base.User", on_delete=models.CASCADE, related_name='+', default='A99999')
    access_user      = models.ForeignKey("base.User", on_delete=models.CASCADE, related_name='+', default='A99999')
    client_ip        = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False, default='')
    string01         = models.CharField(max_length=255, blank=False, unique=False, primary_key=False, default='')
    string02         = models.CharField(max_length=255, blank=False, unique=False, primary_key=False, default='')
    string03         = models.CharField(max_length=255, blank=False, unique=False, primary_key=False, default='')
    string04         = models.CharField(max_length=255, blank=False, unique=False, primary_key=False, default='')
    string05         = models.CharField(max_length=255, blank=False, unique=False, primary_key=False, default='')
    string06         = models.CharField(max_length=255, blank=False, unique=False, primary_key=False, default='')
    string07         = models.CharField(max_length=255, blank=False, unique=False, primary_key=False, default='')
    text01           = models.TextField(blank=False, unique=False, primary_key=False, default='')
    text02           = models.TextField(blank=False, unique=False, primary_key=False, default='')
    text03           = models.TextField(blank=False, unique=False, primary_key=False, default='')
    list01           = models.TextField(blank=False, unique=False, primary_key=False, default='')
    list02           = models.TextField(blank=False, unique=False, primary_key=False, default='')
    list03           = models.TextField(blank=False, unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_parameter'
        verbose_name_plural = 'parameters (base_parameter)'
        ordering            = []
        
    def __str__(self):
        return 'parameter'
# AUTOGEN_END_Parameter#


# AUTOGEN_BEGIN_Person#
class Person(BaseModel):
    person_id        = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    client           = models.ForeignKey("static.Client", on_delete=models.CASCADE, related_name='+', default='999')
    gender_type      = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='700')
    grouping         = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False, default='')
    order_by         = models.CharField(max_length=  2, blank=True , unique=False, primary_key=False, default='99')
    code             = models.CharField(max_length= 15, blank=True , unique=False, primary_key=False)
    salutation       = models.CharField(max_length=  8, blank=True , unique=False, primary_key=False, default='', help_text="mr., mrs....")
    first_name       = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    middle_name      = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    last_name        = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    birth_date       = models.DateTimeField(default=beginning_of_time)
    email            = models.TextField(blank=True , unique=False, primary_key=False, default='')
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
        return ModelUtil.get_full_name(self.last_name, self.first_name, self.middle_name, self.salutation)
# AUTOGEN_END_Person#


# AUTOGEN_BEGIN_PosMenu#
class PosMenu(BaseModel):
    pos_menu_id         = models.CharField(max_length=  4, blank=False, unique=True , primary_key=True )
    hotel               = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    category            = models.ForeignKey("base.Category", on_delete=models.CASCADE, related_name='+', default='A9999')
    currency            = models.ForeignKey("static.Currency", on_delete=models.CASCADE, related_name='+', default='00')
    menu_start_date     = models.DateTimeField(default=today)
    menu_end_date       = models.DateTimeField(default=end_of_time)
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='021')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_pos_menu'
        verbose_name_plural = 'Pont of Sale Menus (base_pos_menu)'
        ordering            = []
        
    def __str__(self):
        return 'pos_menu'
# AUTOGEN_END_PosMenu#


# AUTOGEN_BEGIN_PosMenuItem#
class PosMenuItem(BaseModel):
    pos_menu_item_id = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    pos_menu         = models.ForeignKey("base.PosMenu", on_delete=models.CASCADE, related_name='+')
    item             = models.ForeignKey("base.Item", on_delete=models.CASCADE, related_name='+')
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='00L')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    price            = models.DecimalField(max_digits= 11, decimal_places=  2, blank=False, unique=False, primary_key=False, default=0.00)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_pos_menu_item'
        verbose_name_plural = 'pos_menu/item junction (base_pos_menu_item)'
        ordering            = []
        
    def __str__(self):
        return 'pos_menu_item'
# AUTOGEN_END_PosMenuItem#


# AUTOGEN_BEGIN_Position#
class Position(BaseModel):
    position_id        = models.CharField(max_length=  5, blank=False, unique=True , primary_key=True )
    parent_position    = models.ForeignKey("self", on_delete=models.CASCADE, to_field='position_id', related_name="+", db_column="parent_position_id", default=None, null=True)
    type               = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status             = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    hotel              = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name="+", default='A000')
    code               = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False, default='')
    description        = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    email              = models.TextField(blank=False, unique=False, primary_key=False, default='')
    grouping           = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False, default='')
    position_key       = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    static_flag        = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment   = models.TextField(blank=True , unique=False, primary_key=False)
    created_date       = models.DateTimeField(auto_now_add=True)
    last_updated       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_position'
        verbose_name_plural = 'Positions (base_position)'
        ordering            = []
        
    def __str__(self):
        return 'position'
# AUTOGEN_END_Position#


# AUTOGEN_BEGIN_Role#
class Role(BaseModel):
    role_id          = models.CharField(max_length=  4, blank=False, unique=True , primary_key=True )
    parent_role      = models.ForeignKey("self", on_delete=models.CASCADE, to_field='role_id', related_name="+", db_column="parent_role_id", default=None, null=True)
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    hotel            = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    grouping         = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    code             = models.CharField(max_length= 10, blank=True , unique=False, primary_key=False, default='')
    description      = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    role_key         = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    group1           = models.CharField(max_length= 15, blank=True , unique=False, primary_key=False, default='')
    group2           = models.CharField(max_length= 15, blank=True , unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_role'
        verbose_name_plural = 'roles (base_role)'
        ordering            = []
        
    def __str__(self):
        return 'role'
# AUTOGEN_END_Role#


# AUTOGEN_BEGIN_RoleProcess#
class RoleProcess(BaseModel):
    role_process_id  = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    role             = models.ForeignKey("base.Role", on_delete=models.CASCADE, related_name="+", default='A999')
    process          = models.ForeignKey("static.Process", on_delete=models.CASCADE, related_name="+", default='A00000')
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    can_create       = models.BooleanField(default=False)
    can_read         = models.BooleanField(default=False)
    can_update       = models.BooleanField(default=False)
    can_delete       = models.BooleanField(default=False)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_role_process'
        verbose_name_plural = 'Role/Process junction (base_role_process)'
        ordering            = []
        
    def __str__(self):
        return 'role_process'
# AUTOGEN_END_RoleProcess#


# AUTOGEN_BEGIN_User#
class User(AbstractUser, BaseModel):
    user_id                = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    access_user_id         = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False, default='')
    type                   = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='041')
    status                 = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    verification_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    person                 = models.ForeignKey("base.Person", on_delete=models.CASCADE, default='A9999')
    grouping               = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False, default='')
    code                   = models.CharField(max_length= 10, blank=True , unique=False, primary_key=False)
    description            = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    # username               = models.CharField(max_length=150, blank=True , unique=False, primary_key=False)
    # password               = models.CharField(max_length=100, blank=True , unique=False, primary_key=False, null=True)
    # is_staff               = models.BooleanField(default=True)
    # is_active              = models.BooleanField(default=True)
    # is_superuser           = models.BooleanField(default=False)
    user_key               = models.CharField(max_length= 50, blank=True , unique=False, primary_key=False, default='')
    start_date             = models.DateTimeField(default=today)
    end_date               = models.DateTimeField(default=end_of_time)
    effective_status       = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", db_column="effective_status_id", default='021')
    static_flag            = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    external_id            = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False)
    internal_comment       = models.TextField(blank=True , unique=False, primary_key=False)
    created_date           = models.DateTimeField(auto_now_add=True)
    last_updated           = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_user'
        verbose_name_plural = 'users (base_user)'
        ordering            = []
        
    def __str__(self):
        return self.code + ' ' + self.description
# AUTOGEN_END_User#


# AUTOGEN_BEGIN_UserHotel#
class UserHotel(BaseModel):
    user_hotel_id       = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    user                = models.ForeignKey("base.User", on_delete=models.CASCADE, related_name='userHotels', default='001')
    hotel               = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A00000')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", db_column="effective_status_id", default='021')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_user_hotel'
        verbose_name_plural = 'user hotels junction (base_user_hotel)'
        ordering            = []
        
    def __str__(self):
        return 'user_hotel'
# AUTOGEN_END_UserHotel#


# AUTOGEN_BEGIN_UserRole#
class UserRole(BaseModel):
    user_role_id        = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    user                = models.ForeignKey("base.User", on_delete=models.CASCADE, related_name='+')
    role                = models.ForeignKey("base.Role", on_delete=models.CASCADE, related_name='+')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    access_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='')
    start_date          = models.DateTimeField(default=timezone.now)
    end_date            = models.DateTimeField(default=timezone.now)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", db_column="effective_status_id", default='021')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_user_role'
        verbose_name_plural = 'user roles (base_user_role)'
        ordering            = []
        
    def __str__(self):
        return 'user_role'
# AUTOGEN_END_UserRole#


# AUTOGEN_BEGIN_UserVerification#
class UserVerification(BaseModel):
    user_verfication_id = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    user                = models.ForeignKey("base.User", on_delete=models.CASCADE, related_name='+')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    email_sent_date     = models.DateTimeField(default=end_of_time)
    verification_date   = models.DateTimeField(default=end_of_time)
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'base_user_verification'
        verbose_name_plural = 'user verification (base_user_verification)'
        ordering            = []
        
    def __str__(self):
        return 'user_verification'
# AUTOGEN_END_UserVerification#


