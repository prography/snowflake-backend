from django.apps import AppConfig


class LabsConfig(AppConfig):
    name = 'labs'

    def ready(self):
        import labs.signals
