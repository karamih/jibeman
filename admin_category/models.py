from django.db import models
from django_jalali.db import models as jmodels


class DefaultCategoryModel(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    name = models.CharField(max_length=30)
    icon_name = models.CharField(max_length=30)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    icon_fg_color = models.CharField(max_length=6)
    icon_bg_color = models.CharField(max_length=6)
    is_default = models.BooleanField(default=False)
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'default_categories'
        verbose_name = 'Default Category'
        verbose_name_plural = 'Default Categories'
        unique_together = ('name', 'transaction_type', 'is_default')

    def __str__(self):
        return self.name
