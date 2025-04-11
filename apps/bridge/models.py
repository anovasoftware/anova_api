from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
# from .models_extended import *


# AUTOGEN_BEGIN_Manifest#
class Manifest(BaseModel):
    manifest_id           = models.CharField(max_length=  6, blank=False, unique=True , primary_key=True )
    type                  = models.ForeignKey("static.Type", on_delete=models.CASCADE, related_name='+', default='000')
    status                = models.ForeignKey("static.Status", on_delete=models.CASCADE, related_name='+', default='001')
    hotel                 = models.ForeignKey("static.Hotel", on_delete=models.CASCADE, related_name='+', default='A000')
    res_identifier        = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False)
    res_status_identifier = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False)
    channel_identifier    = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False)
    booking_platform      = models.CharField(max_length= 25, blank=False, unique=False, primary_key=False)
    check_in_date         = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False)
    check_out_date        = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False)
    room_number           = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False)
    room_type             = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False)
    guest_identifier      = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False)
    first_name            = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False)
    last_name             = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False)
    email                 = models.CharField(max_length= 35, blank=False, unique=False, primary_key=False)
    gender                = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False)
    birth_date            = models.CharField(max_length= 10, blank=False, unique=False, primary_key=False)
    mobile_phone_number   = models.CharField(max_length= 15, blank=False, unique=False, primary_key=False)
    nationality           = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False)
    document_number       = models.CharField(max_length= 20, blank=False, unique=False, primary_key=False)
    document_type         = models.CharField(max_length=  6, blank=False, unique=False, primary_key=False)
    static_flag           = models.CharField(max_length=  1, blank=True , unique=False, primary_key=False, default='N')
    internal_comment      = models.TextField(blank=True , unique=False, primary_key=False)
    created_date          = models.DateTimeField(auto_now_add=True)
    last_updated          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'bridge_manifest'
        verbose_name_plural = 'manifest (bridge_manifest)'
        ordering            = []
        
    def __str__(self):
        return 'manifest'
# AUTOGEN_END_Manifest#


