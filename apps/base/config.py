import os
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.backends.signals import connection_created

class BaseConfig(AppConfig):
    name = 'apps.base'

    # def ready(self):
    #     from apps.base.utilities.hotel_utilities import load_hotel_types
    #     # Connect the signal to the populate_tables functionload_hotel_types
    #     connection_created.connect(load_hotel_types)

