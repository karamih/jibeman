import jdatetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from client_account.models import AccountModel
from client_transaction.models import TransactionModel
from client_category.models import CategoryModel


class BudgetModel(models.Model):
    current_date = jdatetime.date.today()
    start_date = current_date.replace(day=1)
    end_date = (current_date + jdatetime.timedelta(days=30)).replace(day=1) - jdatetime.timedelta(days=1)

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
    name = models.CharField(max_length=30, error_messages='نام انتخابی نهایت 30 کاراکتر است.')
    amount = models.DecimalField(max_digits=16, decimal_places=0, error_messages='سقف بودجه بندی 16 رقم است.')
    cycle_start_date = jmodels.jDateField(default=start_date)
    cycle_end_date = jmodels.jDateField(default=end_date)
    remaining = models.DecimalField(max_digits=16, decimal_places=0, error_messages='سقف بودجه بندی 16 رقم است.')
    alarm_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name="Alarm Percent",
        error_messages='درصد هشدار برای باقی مانده بودجه بندی بین 1 الی 99 درصد است.'
    )
    is_closed = models.BooleanField(default=False)

    class Meta:
        db_table = 'budgets'
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        unique_together = ['account', 'name', 'category', 'cycle_start_date']

    def __str__(self):
        return f"{self.account.name} - {self.category.name} - {self.amount}"

    def clean(self):
        if self.category and self.category.transaction_type != 'Expense':
            raise ValidationError('دسته بندی انتخاب شده، برای بودجه بندی مناسب نمی باشد.')

    def update_remaining(self):
        total_expenses = TransactionModel.objects.filter(
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

    def close_budget(self):
        self.is_closed = True
        self.save()

    @staticmethod
    def close_old_budgets():
        today = jdatetime.date.today()
        closed_budgets = BudgetModel.objects.filter(
            cycle_end_date__lt=today,
            is_closed=False
        )
        for budget in closed_budgets:
            budget.close_budget()
