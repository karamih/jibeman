from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FinancialSourceModel


@receiver(post_save, sender=FinancialSourceModel)
def update_account_credit(sender, instance, **kwargs):
    if instance.is_calculate:
        instance.account.update_credit()
