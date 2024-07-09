from django.apps import AppConfig


class SourceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "client_source"

    def ready(self):
        import client_source.signals
