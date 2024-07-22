from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import FinancialSourceModel


@receiver(pre_save, sender=FinancialSourceModel)
def handle_is_calculate_change(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = FinancialSourceModel.objects.get(pk=instance.pk)
        if previous_instance.is_calculate != instance.is_calculate:
            previous_instance.account.update_credit()


@receiver(post_save, sender=FinancialSourceModel)
def update_account_credit_on_save(sender, instance, **kwargs):
    if instance.is_calculate:
        instance.account.update_credit()


@receiver(post_delete, sender=FinancialSourceModel)
def update_account_credit_on_delete(sender, instance, **kwargs):
    if instance.is_calculate:
        instance.account.update_credit()
