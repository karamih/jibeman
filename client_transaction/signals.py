from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TransactionModel


@receiver(post_save, sender=TransactionModel)
def update_financial_sources(sender, instance, created, **kwargs):
    if created:
        if instance.transaction_type == 'Income':
            instance.destination.remain += instance.amount
            instance.destination.save()
        elif instance.transaction_type == 'Expense':
            if instance.budget:
                instance.budget.update_remaining()
            instance.source.remain -= instance.amount
            instance.source.save()
        elif instance.transaction_type == 'Transfer':
            instance.source.remain -= instance.amount
            instance.source.save()
            instance.destination.remain += instance.amount
            instance.destination.save()
