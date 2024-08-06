from django.db import models
from django_jalali.db import models as jmodels
from client_auth.models import ProfileModel


class NotificationModel(models.Model):
    profile = models.ForeignKey(to=ProfileModel, related_name='notifications', verbose_name='profile',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    message = models.CharField(max_length=100)
    created_time = jmodels.jDateTimeField(auto_now_add=True)
    expires_at = jmodels.jDateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return self.title
