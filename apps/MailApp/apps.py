from django.apps import AppConfig


class MailAppConfig(AppConfig):
    name = 'MailApp'

    def ready(self):
        from . import signals
