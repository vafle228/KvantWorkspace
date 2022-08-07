from django.apps import AppConfig


class LoginAppConfig(AppConfig):
    name = 'LoginApp'

    def ready(self) -> None:
        from . import signals
