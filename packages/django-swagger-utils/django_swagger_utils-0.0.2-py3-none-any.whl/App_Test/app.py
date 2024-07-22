
from django.apps import AppConfig


class App_TestAppConfig(AppConfig):
    name = "App_Test"

    def ready(self):
        from App_Test import signals # pylint: disable=unused-variable
