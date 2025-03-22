from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
# from .models_extended import *


# AUTOGEN_BEGIN_Category#
class Category(BaseModel):
    category_id         = models.CharField(max_length=  5, blank=False, unique=True , primary_key=True )
    hotel               = models.ForeignKey("res.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name="+", default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='001')
    parent_category     = models.ForeignKey("self", on_delete=models.CASCADE, to_field='category_id', related_name="+", db_column="parent_category_id", default=None, null=True)
    order_by            = models.CharField(max_length=  2, blank=False, unique=False, primary_key=False, default='99')
    code                = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False, default='')
    description         = models.CharField(max_length= 90, blank=False, unique=False, primary_key=False)
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", db_column="effective_status_id", default='021')
    grouping            = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False, default='')
    category_key        = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False)
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_category'
        verbose_name_plural = 'res categories (res_category)'
        ordering            = []
        
    def __str__(self):
        return 'category'
# AUTOGEN_END_Category#


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
        db_table            = 'res_hotel'
        verbose_name_plural = 'hotels/cruise ships (res_hotel)'
        ordering            = []
        
    def __str__(self):
        return 'hotel'
# AUTOGEN_END_Hotel#


# AUTOGEN_BEGIN_Reservation#
class Reservation(BaseModel):
    reservation_id           = models.CharField(max_length=  5, blank=False, unique=True , primary_key=True )
    hotel                    = models.ForeignKey("res.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    type                     = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status                   = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    travel_agency_company    = models.ForeignKey("base.Company", on_delete=models.CASCADE, related_name='+', default='A0000')
    person                   = models.ForeignKey("base.Person", on_delete=models.CASCADE, related_name='+', default='A00000')
    static_flag              = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment         = models.TextField(blank=True , unique=False, primary_key=False)
    created_date             = models.DateTimeField(auto_now_add=True)
    last_updated             = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_reservation'
        verbose_name_plural = 'reservation table (res_reservation)'
        ordering            = []
        
    def __str__(self):
        return 'reservation'
# AUTOGEN_END_Reservation#


# AUTOGEN_BEGIN_Room#
class Room(BaseModel):
    room_id             = models.CharField(max_length=  4, blank=False, unique=True , primary_key=True )
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='999')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    client              = models.ForeignKey("static.Client", on_delete=models.CASCADE, related_name='+', default='999')
    hotel               = models.ForeignKey("res.Hotel", on_delete=models.CASCADE, related_name='+')
    category            = models.ForeignKey("res.Category", on_delete=models.CASCADE, related_name='+', default='A9999')
    order_by            = models.CharField(max_length=  2, blank=False, unique=False, primary_key=False, default='99')
    code                = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False, default='')
    description         = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    start_date          = models.DateTimeField(default=beginning_of_time)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='021')
    grouping            = models.CharField(max_length= 30, blank=False, unique=False, primary_key=False, default='')
    room_key            = models.CharField(max_length= 50, blank=False, unique=False, primary_key=False, default='')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_room'
        verbose_name_plural = 'rooms (res_room)'
        ordering            = []
        
    def __str__(self):
        return 'room'
# AUTOGEN_END_Room#


