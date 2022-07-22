from django.apps import AppConfig


class ProjectAppConfig(AppConfig):
    name = 'ProjectApp'

    def ready(self):
        from . import signals
