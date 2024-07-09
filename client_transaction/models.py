from django.db import models
from django_jalali.db import models as jmodels
from django.core.exceptions import ValidationError
from client_budget.models import BudgetModel
from client_source.models import FinancialSourceModel
from django.utils import timezone
from client_category.models import CategoryModel


class TransactionModel(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Transfer', 'Transfer'),
    ]
    TRANSACTION_LEVEL_CHOICES = [
        ('normal', 'Normal Transaction'),
        ('unnecessary', 'Unnecessary Transaction')
    ]

    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES)
    category = models.ForeignKey(
        to=CategoryModel,
        related_name='transactions',
        verbose_name='category',
        on_delete=models.PROTECT
    )
    source = models.ForeignKey(
        to=FinancialSourceModel,
        related_name='transactions_as_source',
        verbose_name='source',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    destination = models.ForeignKey(
        to=FinancialSourceModel,
        related_name='transactions_as_destination',
        verbose_name='destination',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=16, decimal_places=0)
    transaction_level = models.CharField(max_length=11, default='normal', choices=TRANSACTION_LEVEL_CHOICES)
    fee = models.DecimalField(max_digits=16, decimal_places=0, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True)
    date = jmodels.jDateField()
    time = models.TimeField(blank=True, null=True)
    created_time = jmodels.jDateField(auto_now_add=True)
    budget = models.ForeignKey(
        to=BudgetModel,
        related_name='transactions',
        verbose_name='budget',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'transaction'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def clean(self):
        if self.transaction_type == 'Income' and not self.destination:
            raise ValidationError('Income transactions must have a destination financial source.')
        elif self.transaction_type == 'Expense' and not self.source:
            raise ValidationError('Expense transactions must have a source financial source.')
        elif self.transaction_type == 'Transfer' and (not self.source or not self.destination):
            raise ValidationError('Transfer transactions must have both source and destination financial sources.')
        elif self.transaction_type != 'Transfer' and self.source and self.destination:
            raise ValidationError(
                'Non-transfer transactions should not have both source and destination financial sources.')

        user_transactions = TransactionModel.objects.filter(
            source__account__profile=self.source.account.profile)
        if user_transactions is None:
            user_transactions = TransactionModel.objects.filter(
                destination__account__profile=self.destination.account.profile)

        today = timezone.now().date()
        start_of_month = today.replace(day=1)

        daily_transactions = user_transactions.filter(date=today).count()
        monthly_transactions = user_transactions.filter(date__gte=start_of_month).count()

        if daily_transactions >= 1000:
            raise ValidationError('You have reached the maximum number of transactions for today (1000).')

        if monthly_transactions >= 15000:
            raise ValidationError('You have reached the maximum number of transactions for this month (15000).')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
