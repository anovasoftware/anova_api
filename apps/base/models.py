from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from core.utilities.date_utilities import beginning_of_time, end_of_time, today
from core.models import BaseModel
# from .models_extended import *


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


