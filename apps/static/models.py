from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
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


# AUTOGEN_BEGIN_Status#
class Status(BaseModel):
    status_id        = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    grouping         = models.CharField(max_length= 30, blank=True , unique=False, primary_key=False)
    code             = models.CharField(max_length= 10, blank=True , unique=False, primary_key=False)
    description      = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False)
    status_key       = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
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


