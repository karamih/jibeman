from django.db import models
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels

from client_account.models import AccountModel


class CategoryModel(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Transfer', 'Transfer'),
    ]

    account = models.ForeignKey(
        to=AccountModel,
        related_name='categories',
        verbose_name='account',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=30)
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES)
    is_default = models.BooleanField(default=False)
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('account', 'name', 'transaction_type')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.is_default:
            raise ValidationError("دسته بندی پیش فرض قابل حذف نمی باشد.")
        super().delete(*args, **kwargs)
