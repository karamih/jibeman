from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_jalali.db import models as jmodels
from client_account.models import AccountModel
from client_category.models import CategoryModel


class BudgetModel(models.Model):
    account = models.ForeignKey(
        to=AccountModel,
        related_name='budgets',
        verbose_name='account',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        to=CategoryModel,
        related_name='budgets',
        verbose_name='category',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=16, decimal_places=0)
    cycle_start_date = jmodels.jDateField()
    cycle_end_date = jmodels.jDateField()
    remaining = models.DecimalField(max_digits=16, decimal_places=0, default=0)
    alarm_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name="Alarm Percent"
    )

    class Meta:
        db_table = 'budget'
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return f"{self.account.name} - {self.category.name} - {self.amount}"

    def update_remaining(self):
        total_expenses = self.transactions.filter(
            transaction_type='Expense',
            created_time__range=(self.cycle_start_date, self.cycle_end_date)
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        self.remaining = self.amount - total_expenses
        self.save()

        alarm_threshold = self.amount * (self.alarm_percent / 100)
        if self.remaining <= alarm_threshold:
            self.send_alarm_notification()

    def send_alarm_notification(self):
        print(f"Alarm: Budget for {self.category.name} on account {self.account.name} has reached the threshold.")
