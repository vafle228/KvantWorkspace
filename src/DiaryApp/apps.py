from django.apps import AppConfig


class DiaryAppConfig(AppConfig):
    name = 'DiaryApp'

    def ready(self):
        from . import signals
