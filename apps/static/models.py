from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
# from .models_extended import *


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


