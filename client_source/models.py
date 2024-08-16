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
    icon_name = models.CharField(blank=True, null=True, max_length=30)
    icon_color = models.CharField(blank=True, null=True, max_length=6)
    is_calculate = models.BooleanField(default=True)
    is_enable = models.BooleanField(default=True)
    remain = models.IntegerField(default=0)
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'sources'
        verbose_name = 'Financial Source'
        verbose_name_plural = 'Financial Sources'
        constraints = [
            models.UniqueConstraint(fields=['account', 'name'], name='unique_account_name',
                                    violation_error_message='منبع مالی با این نام برای این جساب موجود است.')
        ]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def clean(self):
        super().clean()
        if self.type == 'Card':
            if not self.card_number:
                raise ValidationError({'card_number': 'وقتی منبع مالی کارت بانکی است، شماره کارت الزامی است.'})
            elif self.icon_name:
                raise ValidationError({'icon_name': 'وقتی منبع مالی کارت بانکی است، نام آیکون نباید ارسال شود.'})
            elif self.icon_color:
                raise ValidationError({'icon_color': 'وقتی منبع مالی کارت بانکی است، رنگ آیکون نباید ارسال شود.'})
        elif self.type == 'Cash':
            if self.card_number:
                raise ValidationError({'card_number': 'وقتی منبع مالی پول نقد است، شماره کارت نباید ارسال شود.'})
            elif not self.icon_name:
                raise ValidationError({'icon_name': 'وقتی منبع مالی پول نقد است، نام آیکون الزامی است.'})
            elif not self.icon_color:
                raise ValidationError({'icon_color': 'وقتی منبع مالی پول نقد است، رنگ آیکون الزامی است.'})

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
