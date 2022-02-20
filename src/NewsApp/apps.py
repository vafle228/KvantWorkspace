from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    name = 'NewsApp'

    def ready(self):
        from . import signals
