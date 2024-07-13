from django.db import models
from django_jalali.db import models as jmodels
from client_auth.models import ProfileModel


class NotificationModel(models.Model):
    profile = models.ForeignKey(to=ProfileModel, related_name='notifications', verbose_name='profile',
                                on_delete=models.CASCADE)
    notification = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    created_time = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"Notification for {self.profile.user.phone_number}"


