import jdatetime
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import TransactionModel
from client_budget.models import BudgetModel
from django.db import transaction


@receiver(pre_save, sender=TransactionModel)
def handle_transaction_update(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = TransactionModel.objects.get(pk=instance.pk)
        if previous_instance.amount != instance.amount or previous_instance.transaction_type != instance.transaction_type:
            instance.source.update_credit()


@receiver(post_save, sender=TransactionModel)
def update_financial_sources_on_save(sender, instance, created, **kwargs):
    with transaction.atomic():
        instance.source.update_credit()

        if instance.transaction_type == 'Expense' and instance.category:
            today = jdatetime.date.today()
            budget = BudgetModel.objects.filter(
                account=instance.source.account,
                category=instance.category,
                cycle_start_date__lte=today,
                cycle_end_date__gte=today,
                is_closed=False
            ).first()
            if budget:
                budget.update_remaining()

        BudgetModel.close_old_budgets()


@receiver(post_delete, sender=TransactionModel)
def update_financial_sources_on_delete(sender, instance, **kwargs):
    with transaction.atomic():
        instance.source.update_credit()

        if instance.transaction_type == 'Expense' and instance.category:
            today = jdatetime.date.today()
            budget = BudgetModel.objects.filter(
                account=instance.source.account,
                category=instance.category,
                cycle_start_date__lte=today,
                cycle_end_date__gte=today,
                is_closed=False
            ).first()
            if budget:
                budget.update_remaining()

        BudgetModel.close_old_budgets()
