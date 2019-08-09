from importlib import import_module

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Заявки на ремонт'

    def ready(self):
        import_module('core.handlers')
