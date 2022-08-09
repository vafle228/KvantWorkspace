from django.apps import AppConfig


class RegisterAppConfig(AppConfig):
    name = 'RegisterApp'

    def ready(self):
        from . import signals
