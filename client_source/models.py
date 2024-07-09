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
        message="Card number must be exactly 16 digits."
    )

    account = models.ForeignKey(
        to=AccountModel,
        related_name='financial_sources',
        verbose_name='account',
        on_delete=models.CASCADE)
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
            raise ValidationError({'card_number': 'Card number is required when the type is Card.'})
        elif self.type != 'Card' and self.card_number:
            raise ValidationError({'card_number': 'Card number is unavailable when the type is Cash.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
