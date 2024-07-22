from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_jalali.db import models as jmodels

from client_account.models import AccountModel


class FinancialSourceModel(models.Model):
    FinancialSourceType = [
        ('Card', 'Card'),
        ('Cash', 'Cash'),
    ]

    card_number_validator = RegexValidator(
        regex=r'^\d{16}$',
        message="شماره کارت بایستی 16 رقم باشد."
    )

    account = models.ForeignKey(
        to=AccountModel,
        related_name='financial_sources',
        verbose_name='account',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=4, choices=FinancialSourceType)
    card_number = models.CharField(blank=True, null=True, validators=[card_number_validator])
    is_calculate = models.BooleanField(default=True)
    is_enable = models.BooleanField(default=True)
    remain = models.PositiveBigIntegerField(default=0)
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'financial source'
        verbose_name = 'Financial Source'
        verbose_name_plural = 'Financial Sources'
        constraints = [
            models.UniqueConstraint(fields=['account', 'name'], name='unique_account_name',
                                    violation_error_message='منبع مالی با این نام برای این جساب موجود است.'),
            models.UniqueConstraint(fields=['account', 'card_number'], name='unique_account_card_number',
                                    violation_error_message='منبع مالی با این شماره کارت برای این جساب موجود است.')
        ]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def clean(self):
        super().clean()
        if self.type == 'Card' and not self.card_number:
            raise ValidationError({'card_number': 'وقتی منبع مالی کارت بانکی است، شماره کارت الزامی است.'})
        elif self.type != 'Card' and self.card_number:
            raise ValidationError({'card_number': 'وقتی منبع مالی پول نقد است، شماره کارت نباید ارسال شود.'})

    def update_credit(self):
        total_income = self.transaction.filter(transaction_type='Income').aggregate(models.Sum('amount'))[
                           'amount__sum'] or 0
        total_expense = self.transaction.filter(transaction_type='Expense').aggregate(models.Sum('amount'))[
                           'amount__sum'] or 0
        self.remain = total_income - total_expense
        self.save()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
