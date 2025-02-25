import os
from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'apps.base'
    # path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # print(path)