from django.apps import AppConfig


class TransactionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "client_transaction"

    def ready(self):
        import client_transaction.signals
