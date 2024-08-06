from django.db import models
from django_jalali.db import models as jmodels


class BankModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    numbers = models.JSONField()
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'banks'
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'

    def __str__(self):
        return self.name


class TransactionTypeModel(models.Model):
    bank = models.ForeignKey(BankModel, related_name='transaction_types', on_delete=models.CASCADE)
    type_id = models.IntegerField()
    type_name = models.CharField(max_length=255)
    type_identity = models.CharField(max_length=255, null=True, blank=True)

    amount_format = models.CharField(max_length=255, blank=True)
    amount_after_char = models.IntegerField(default=-1)
    amount_before_char = models.IntegerField(default=-1)
    amount_regex = models.CharField(max_length=255)

    account_number_format = models.CharField(max_length=255, blank=True)
    account_number_after_char = models.IntegerField(default=-1)
    account_number_before_char = models.IntegerField(default=-1)
    account_number_regex = models.CharField(max_length=255)

    date_format = models.CharField(max_length=255, blank=True)
    date_after_char = models.IntegerField(default=-1)
    date_before_char = models.IntegerField(default=-1)
    date_regex = models.CharField(max_length=255)

    time_format = models.CharField(max_length=255, blank=True)
    time_after_char = models.IntegerField(default=-1)
    time_before_char = models.IntegerField(default=-1)
    time_regex = models.CharField(max_length=255)

    description = models.CharField(max_length=255, null=True, blank=True)
    template = models.TextField()

    class Meta:
        db_table = 'transaction_types'
        verbose_name = 'Transaction Type'
        verbose_name_plural = 'Transaction Types'

    def __str__(self):
        return f"{self.bank.name} - {self.type_name}"
