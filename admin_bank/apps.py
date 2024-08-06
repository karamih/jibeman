from django.apps import AppConfig


class AdminBankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_bank'

    def ready(self):
        import admin_bank.signals
