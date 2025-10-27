from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
# from .models_extended import *


# AUTOGEN_BEGIN_Event#
class Event(BaseModel):
    event_id            = models.CharField(max_length=  6, blank=False, unique=False, primary_key=True )
    parent_event        = models.ForeignKey("self", on_delete=models.CASCADE, to_field='event_id', related_name="+", db_column="parent_event_id", default=None, null=True)
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    client              = models.ForeignKey("static.Client", on_delete=models.CASCADE, related_name='+', default='999')
    hotel               = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    code                = models.CharField(max_length= 15, blank=True , unique=False, primary_key=False)
    description         = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False)
    event_start_date    = models.DateTimeField(default=beginning_of_time)
    event_end_date      = models.DateTimeField(default=end_of_time)
    start_date          = models.DateTimeField(default=today)
    end_date            = models.DateTimeField(default=end_of_time)
    effective_status    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", db_column="effective_status_id", default='021')
    grouping            = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    event_key           = models.CharField(max_length= 70, blank=False, unique=False, primary_key=False, default='')
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_event'
        verbose_name_plural = 'events (res_event)'
        ordering            = []
        
    def __str__(self):
        return 'event'
# AUTOGEN_END_Event#


# AUTOGEN_BEGIN_Guest#
class Guest(BaseModel):
    guest_id                  = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    reservation               = models.ForeignKey("res.Reservation", on_delete=models.CASCADE, related_name='+')
    type                      = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status                    = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    person                    = models.ForeignKey("base.Person", on_delete=models.CASCADE, related_name='+', default='A00000')
    responsible_guest         = models.ForeignKey("res.Guest", on_delete=models.CASCADE, related_name="+", default=None, null=True)
    grouping                  = models.CharField(max_length= 40, blank=True , unique=False, primary_key=False, default='')
    guest_key                 = models.CharField(max_length= 70, blank=False, unique=False, primary_key=False, default='')
    authorized_to_charge_flag = models.CharField(max_length=  1, blank=False, unique=False, primary_key=False, default='N')
    static_flag               = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment          = models.TextField(blank=True , unique=False, primary_key=False)
    created_date              = models.DateTimeField(auto_now_add=True)
    last_updated              = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_guest'
        verbose_name_plural = 'guests (res_guest)'
        ordering            = []
        
    def __str__(self):
        return 'guest'
# AUTOGEN_END_Guest#


# AUTOGEN_BEGIN_GuestRoom#
class GuestRoom(BaseModel):
    guest_room_id    = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    guest            = models.ForeignKey("res.Guest", on_delete=models.CASCADE, related_name='+')
    room             = models.ForeignKey("res.Room", on_delete=models.CASCADE, related_name='+', default='A000')
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    arrival_date     = models.DateTimeField(default=end_of_time)
    departure_date   = models.DateTimeField(default=end_of_time)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_guest_room'
        verbose_name_plural = 'guest rooms (res_guest_room)'
        ordering            = []
        
    def __str__(self):
        return 'guest_room'
# AUTOGEN_END_GuestRoom#


# AUTOGEN_BEGIN_HotelItem#
class HotelItem(BaseModel):
    hotel_item_id        = models.CharField(max_length=  3, blank=False, unique=True , primary_key=True )
    hotel                = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    item                 = models.ForeignKey("base.Item", on_delete=models.CASCADE, related_name='+', default='A00000')
    type                 = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    special_item_type    = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    start_date           = models.DateTimeField(default=beginning_of_time)
    end_date             = models.DateTimeField(default=end_of_time)
    effective_status     = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name="+", default='021')
    static_flag          = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment     = models.TextField(blank=True , unique=False, primary_key=False)
    created_date         = models.DateTimeField(auto_now_add=True)
    last_updated         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_hotel_item'
        verbose_name_plural = 'hotel items (special items) (res_hotel_item)'
        ordering            = []
        
    def __str__(self):
        return 'hotel_item'
# AUTOGEN_END_HotelItem#


# AUTOGEN_BEGIN_Reservation#
class Reservation(BaseModel):
    reservation_id           = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    hotel                    = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    type                     = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status                   = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    travel_agency_company    = models.ForeignKey("base.Company", on_delete=models.CASCADE, related_name='+', default='A0000')
    person                   = models.ForeignKey("base.Person", on_delete=models.CASCADE, related_name='+', default='A00000')
    grouping                 = models.CharField(max_length= 15, blank=True , unique=False, primary_key=False, default='')
    reservation_key          = models.CharField(max_length= 25, blank=False, unique=False, primary_key=False, default='')
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
    hotel               = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    category            = models.ForeignKey("base.Category", on_delete=models.CASCADE, related_name='+', default='A9999')
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


# AUTOGEN_BEGIN_Transaction#
class Transaction(BaseModel):
    transaction_id   = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    type             = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status           = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    hotel            = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    event            = models.ForeignKey("res.Event", on_delete=models.CASCADE, related_name='+', default='A00000')
    guest            = models.ForeignKey("res.Guest", on_delete=models.CASCADE, related_name='+')
    server_guest     = models.ForeignKey("res.Guest", on_delete=models.CASCADE, related_name='+')
    description      = models.CharField(max_length= 50, blank=True , unique=False, primary_key=False)
    static_flag      = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment = models.TextField(blank=True , unique=False, primary_key=False)
    created_date     = models.DateTimeField(auto_now_add=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_transaction'
        verbose_name_plural = 'transactions: sales and payments (res_transaction)'
        ordering            = []
        
    def __str__(self):
        return 'transaction'
# AUTOGEN_END_Transaction#


# AUTOGEN_BEGIN_TransactionItem#
class TransactionItem(BaseModel):
    transaction_item_id = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    transaction         = models.ForeignKey("res.Transaction", on_delete=models.CASCADE, related_name='transactionItems')
    item                = models.ForeignKey("base.Item", on_delete=models.CASCADE, related_name='+')
    type                = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status              = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    description         = models.CharField(max_length= 60, blank=True , unique=False, primary_key=False)
    quantity            = models.DecimalField(max_digits= 10, decimal_places=  2, blank=False, unique=False, primary_key=False, default=0.00)
    price               = models.DecimalField(max_digits= 10, decimal_places=  2, blank=False, unique=False, primary_key=False, default=0.00)
    service_rate        = models.DecimalField(max_digits=  8, decimal_places=  4, blank=False, unique=False, primary_key=False, default=0.00)
    discount_rate       = models.DecimalField(max_digits=  8, decimal_places=  4, blank=False, unique=False, primary_key=False, default=0.00)
    discount_flat       = models.DecimalField(max_digits= 10, decimal_places=  2, blank=False, unique=False, primary_key=False, default=0.00)
    allowance           = models.DecimalField(max_digits= 10, decimal_places=  2, blank=False, unique=False, primary_key=False, default=0.00)
    static_flag         = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment    = models.TextField(blank=True , unique=False, primary_key=False)
    created_date        = models.DateTimeField(auto_now_add=True)
    last_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'res_transaction_item'
        verbose_name_plural = 'Transaction Items (res_transaction_item)'
        ordering            = []
        
    def __str__(self):
        return 'transaction_item'
# AUTOGEN_END_TransactionItem#


