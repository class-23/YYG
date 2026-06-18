"""incentive app config"""
from django.apps import AppConfig


class IncentiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.incentive'
    verbose_name = '激励系统'
