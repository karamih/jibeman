import jdatetime
from django.db import models
from django_jalali.db import models as jmodels
from django.core.exceptions import ValidationError
from client_source.models import FinancialSourceModel
from client_category.models import CategoryModel


class TransactionModel(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    TRANSACTION_LEVEL_CHOICES = [
        ('Normal', 'Normal Transaction'),
        ('Unnecessary', 'Unnecessary Transaction')
    ]

    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES)
    category = models.ForeignKey(
        to=CategoryModel,
        related_name='transactions',
        verbose_name='category',
        on_delete=models.CASCADE
    )
    source = models.ForeignKey(
        to=FinancialSourceModel,
        related_name='transaction',
        verbose_name='source',
        on_delete=models.CASCADE,
        error_messages='منبع مالی برای ثبت تراکنش الزامی است.'
    )

    amount = models.DecimalField(max_digits=16, decimal_places=0)
    transaction_level = models.CharField(max_length=11, choices=TRANSACTION_LEVEL_CHOICES, blank=True, null=True)
    is_fee = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    date = jmodels.jDateField()
    time = models.TimeField(blank=True, null=True)
    created_time = jmodels.jDateField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def clean(self):
        if self.category and self.transaction_type != self.category.transaction_type:
            raise ValidationError('دسته بندی انتخاب شده، برای این نوع تراکنش مناسب نمی باشد.')

        user_transactions = TransactionModel.objects.filter(
            source__account__profile=self.source.account.profile)

        today = jdatetime.date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (today + jdatetime.timedelta(days=30)).replace(day=1) - jdatetime.timedelta(days=1)

        daily_transactions = user_transactions.filter(date=today).count()
        monthly_transactions = user_transactions.filter(date__gte=start_of_month, date__lte=end_of_month).count()

        if daily_transactions >= 1000:
            raise ValidationError('شما به سقف ثبت میران تراکنش روزانه (1000) رسیدید.')

        if monthly_transactions >= 15000:
            raise ValidationError('شما به سقف ثبت میزان تراکنش ماهانه (15000) رسیدید.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
