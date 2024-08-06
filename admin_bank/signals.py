import jdatetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TransactionTypeModel


@receiver(post_save, sender=TransactionTypeModel)
@receiver(post_delete, sender=TransactionTypeModel)
def update_bank_updated_time(sender, instance, **kwargs):
    instance.bank.updated_time = jdatetime.datetime.now()
    instance.bank.save()
