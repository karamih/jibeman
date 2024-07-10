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
    remain = models.IntegerField(default=0)
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'financial source'
        verbose_name = 'Financial Source'
        verbose_name_plural = 'Financial Sources'

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def clean(self):
        super().clean()
        if self.type == 'Card' and not self.card_number:
            raise ValidationError({'card_number': 'وقتی منبع مالی کارت بانکی است، شماره کارت الزامی است.'})
        elif self.type != 'Card' and self.card_number:
            raise ValidationError({'card_number': 'وقتی منبع مالی پول نقد است، شماره کارت نباید ارسال شود.'})

        name_exists = FinancialSourceModel.objects.filter(name=self.name, account=self.account).exclude(
            id=self.id).exists()
        if name_exists:
            raise ValidationError({'name': 'منبع مالی با این نام برای این حساب از قبل وجود دارد.'})

        card_exists = FinancialSourceModel.objects.filter(card_number=self.card_number, account=self.account).exclude(
            id=self.id).exists()
        if self.card_number and card_exists:
            raise ValidationError({'card_number': 'منبع مالی با این شماره کارت برای این حساب از قبل وجود دارد.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
