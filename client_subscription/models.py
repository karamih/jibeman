# from django.db import models
#
#
# class SubscriptionModel(models.Model):
#     PLAN_CHOICES = [
#         ('Free', 'Free'),
#         ('Standard', 'Standard'),
#         ('Premium', 'Premium'),
#     ]
#
#     DURATION_CHOICES = [
#         (1, '1 Month'),
#         (3, '3 Months'),
#         (6, '6 Months'),
#         (12, '12 Months'),
#     ]
#
#     plan = models.CharField(max_length=8, choices=PLAN_CHOICES, default='Free')
#     price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
#     duration_month = models.PositiveIntegerField(choices=DURATION_CHOICES, default=1)
#
#     class Meta:
#         db_table = 'subscription'
#         verbose_name = 'Subscription'
#         verbose_name_plural = 'Subscriptions'
#
#     def __str__(self):
#         return f'{self.plan} - {self.duration_month} Months'
