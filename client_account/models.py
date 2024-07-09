from django.db import models
from django_jalali.db import models as jmodels
from client_user.models import ProfileModel


class AccountModel(models.Model):
    profile = models.ForeignKey(
        to=ProfileModel,
        related_name='accounts',
        verbose_name='profile',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30)
    credit = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    updated_time = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def update_credit(self):
        total_credit = self.financial_sources.filter(is_calculate=True).aggregate(models.Sum('remain'))[
                           'remain__sum'] or 0
        self.credit = total_credit
        self.save()

    def __str__(self):
        return f'{self.name} ({self.profile.user.phone_number})'
