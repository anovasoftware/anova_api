from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
# from .models_extended import *


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


