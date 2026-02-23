from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
from core.utilities.database_utilties import ModelUtilities as ModelUtil
# from .models_extended import *


# AUTOGEN_BEGIN_Client#
class Client(BaseModel):
    client_id        = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    parent_client    = models.ForeignKey("self", on_delete=models.CASCADE, to_field='client_id', related_name="+", db_column="parent_client_id", default=None, null=True)
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='004')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    code             = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False)
    description      = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False)
    grouping         = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    client_key       = models.CharField(max_length= 70, blank=False, unique=False, primary_key=False)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_client'
        verbose_name_plural = 'clients (static_client)'
        ordering            = []
        
    def __str__(self):
        return 'client'
# AUTOGEN_END_Client#


# AUTOGEN_BEGIN_Currency#
class Currency(BaseModel):
    currency_id      = models.CharField(max_length=  2, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    code             = models.CharField(max_length=  3, blank=False, unique=False, primary_key=False, default='')
    symbol           = models.CharField(max_length=  3, blank=False, unique=False, primary_key=False, default='')
    description      = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    order_by         = models.CharField(max_length=  2, blank=False, unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_currency'
        verbose_name_plural = 'currencies (static_currency)'
        ordering            = []
        
    def __str__(self):
        return 'currency'
# AUTOGEN_END_Currency#


# AUTOGEN_BEGIN_Form#
class Form(BaseModel):
    form_id                 = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    type                    = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status                  = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    description             = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False, default='')
    header                  = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False, default='')
    data_source_application = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    data_source_model_name  = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    save_button_label       = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    save_button_action      = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='saveAndClose')
    grouping                = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    form_key                = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    static_flag             = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment        = models.TextField(blank=True , unique=False, primary_key=False)
    created_date            = models.DateTimeField(auto_now_add=True)
    last_updated            = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_form'
        verbose_name_plural = 'forms (static_form)'
        ordering            = []
        
    def __str__(self):
        return 'form'
# AUTOGEN_END_Form#


# AUTOGEN_BEGIN_FormExtra#
class FormExtra(BaseModel):
    form_extra_id    = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    form             = models.ForeignKey("static.Form", on_delete=models.CASCADE, related_name='+', default='000')
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    target_form      = models.ForeignKey("static.Form", on_delete=models.CASCADE, related_name='+', default='000')
    order_by         = models.CharField(max_length=  2, blank=False, unique=False, primary_key=False, default='00')
    description      = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    label            = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    grouping         = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False, default='')
    form_extra_key   = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_form_extra'
        verbose_name_plural = 'form extras (static_form_extra)'
        ordering            = []
        
    def __str__(self):
        return 'form_extra'
# AUTOGEN_END_FormExtra#


# AUTOGEN_BEGIN_FormField#
class FormField(BaseModel):
    form_field_id                       = models.CharField(max_length=  5, blank=False, unique=True , primary_key=True )
    form                                = models.ForeignKey("static.Form", on_delete=models.CASCADE, related_name='+', default='000')
    type                                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000', null=True)
    status                              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    order_by                            = models.CharField(max_length=  2, blank=True , unique=False, primary_key=False)
    custom_flag                         = models.CharField(max_length=  1, blank=False, unique=False, primary_key=False, default='N')
    control_type                        = models.CharField(max_length= 15, blank=True , unique=False, primary_key=False, default='')
    tab_name                            = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    label                               = models.CharField(max_length= 90, blank=False, unique=False, primary_key=False, default='')
    name                                = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    mapping_name                        = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    default_value                       = models.CharField(max_length=150, blank=False, unique=False, primary_key=False, default='')
    data_source_application             = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    data_source_model_name              = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    data_source_filter                  = models.TextField(blank=False, unique=False, primary_key=False, default='')
    data_source_filter_effective_status = models.TextField(blank=False, unique=False, primary_key=False, default='')
    data_source_order                   = models.TextField(blank=False, unique=False, primary_key=False, default='')
    display_value                       = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    data_source_fields                  = models.CharField(max_length=150, blank=False, unique=False, primary_key=False, default='')
    data_source_fstring                 = models.CharField(max_length= 90, blank=False, unique=False, primary_key=False, default='')
    data_source_key_field               = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False, default='')
    disabled_create                     = models.BooleanField(default=False)
    disabled_update                     = models.BooleanField(default=False)
    required_flag                       = models.CharField(max_length=  1, blank=False, unique=False, primary_key=False, default='N')
    static_flag                         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment                    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date                        = models.DateTimeField(auto_now_add=True)
    last_updated                        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_form_field'
        verbose_name_plural = 'form fields (static_form_field)'
        ordering            = []
        
    def __str__(self):
        return 'form_field'
# AUTOGEN_END_FormField#


# AUTOGEN_BEGIN_Hotel#
class Hotel(BaseModel):
    hotel_id         = models.CharField(max_length=  4, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='999')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    client           = models.ForeignKey("static.Client", on_delete=models.CASCADE, related_name='+', default='999')
    code             = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False)
    description      = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    vms_identifier   = models.CharField(max_length=  4, blank=False, unique=False, primary_key=False)
    grouping         = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    hotel_key        = models.CharField(max_length= 50, blank=True , unique=False, primary_key=False)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_hotel'
        verbose_name_plural = 'hotels/cruise ships (static_hotel)'
        ordering            = []
        
    def __str__(self):
        return 'hotel'
# AUTOGEN_END_Hotel#


# AUTOGEN_BEGIN_Menu#
class Menu(BaseModel):
    menu_id          = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    parent_menu      = models.ForeignKey("self", on_delete=models.CASCADE, to_field='menu_id', related_name="+", db_column="parent_menu_id", default=None, null=True)
    page             = models.ForeignKey("static.Page", on_delete=models.CASCADE, related_name='+', default=None, null=True)
    order_by         = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False, default='00')
    description      = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False)
    title            = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False)
    sub_title        = models.CharField(max_length= 80, blank=False, unique=False, primary_key=False)
    breadcrumb_name  = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False)
    route            = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False)
    params           = models.TextField(blank=False, unique=False, primary_key=False, default='')
    icon             = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False)
    grouping         = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False)
    menu_key         = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_menu'
        verbose_name_plural = 'menus (static_menu)'
        ordering            = []
        
    def __str__(self):
        return 'menu'
# AUTOGEN_END_Menu#


# AUTOGEN_BEGIN_Page#
class Page(BaseModel):
    page_id          = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    code             = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False, default='')
    description      = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    grouping         = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    page_key         = models.CharField(max_length= 50, blank=True , unique=False, primary_key=False, default='')
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_page'
        verbose_name_plural = 'pages (static_page)'
        ordering            = []
        
    def __str__(self):
        return 'page'
# AUTOGEN_END_Page#


# AUTOGEN_BEGIN_Process#
class Process(BaseModel):
    process_id       = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True , default='')
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    code             = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False, default='')
    description      = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    route            = models.CharField(max_length= 80, blank=False, unique=False, primary_key=False, default='')
    view             = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    module_path      = models.CharField(max_length=100, blank=False, unique=False, primary_key=False, default='')
    grouping         = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    process_key      = models.CharField(max_length= 40, blank=False, unique=False, primary_key=False, default='')
    supports_create  = models.BooleanField(default=False)
    supports_read    = models.BooleanField(default=False)
    supports_update  = models.BooleanField(default=False)
    supports_delete  = models.BooleanField(default=False)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_process'
        verbose_name_plural = 'processes (static_process)'
        ordering            = []
        
    def __str__(self):
        return 'process'
# AUTOGEN_END_Process#


# AUTOGEN_BEGIN_Status#
class Status(BaseModel):
    status_id        = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    grouping         = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False)
    code             = models.CharField(max_length= 10, blank=True , unique=False, primary_key=False)
    description      = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    status_key       = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    status_code      = models.IntegerField(default=0)
    flag1            = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False, default='')
    group1           = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='')
    order_by         = models.CharField(max_length=  2, blank=True , unique=False, primary_key=False, default="99")
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_status'
        verbose_name_plural = 'status (static_status)'
        ordering            = []
        
    def __str__(self):
        return self.status_id + '-' + self.description
# AUTOGEN_END_Status#


# AUTOGEN_BEGIN_Text#
class Text(BaseModel):
    text_id             = models.CharField(max_length=  5, blank=False, unique=False, primary_key=True , default='')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    description         = models.CharField(max_length=100, blank=False, unique=False, primary_key=False)
    description_short   = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False)
    description_long    = models.TextField(blank=False, unique=False, primary_key=False)
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='021')
    grouping            = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False)
    text_key            = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_text'
        verbose_name_plural = 'freeform text including page content (static_text)'
        ordering            = []
        
    def __str__(self):
        return 'text'
# AUTOGEN_END_Text#


# AUTOGEN_BEGIN_Type#
class Type(BaseModel):
    type_id           = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    parent_type       = models.ForeignKey("self", on_delete=models.CASCADE, to_field='type_id', related_name="+", db_column="parent_type_id", default=None, null=True)
    grouping          = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False)
    code              = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    description       = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False)
    description_short = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False)
    description_long  = models.TextField(blank=True , unique=False, primary_key=False, default='')
    description2      = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False)
    type_key          = models.CharField(max_length= 60, blank=False, unique=False, primary_key=False, default='')
    group1            = models.CharField(max_length= 10, blank=True , unique=False, primary_key=False)
    flag1             = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False, default='')
    flag2             = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False, default='')
    attributes        = models.TextField(blank=True , unique=False, primary_key=False, default='')
    order_by          = models.CharField(max_length=  2, blank=True , unique=False, primary_key=False, default="99")
    external_id       = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False)
    static_flag       = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment  = models.TextField(blank=True , unique=False, primary_key=False)
    created_date      = models.DateTimeField(auto_now_add=True)
    last_updated      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'static_type'
        verbose_name_plural = 'types (static_type)'
        ordering            = []
        
    def __str__(self):
        return self.type_id + '-' + self.description
# AUTOGEN_END_Type#


