import jdatetime
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_image(image):
    limit_mb = 5
    if image.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb} MB")
    if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError("Only .jpg, .jpeg, and .png files are allowed")


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('answered', 'Answered'),
    ]

    subject = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets', on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='ticket_images/', blank=True, null=True, validators=[validate_image])
    image2 = models.ImageField(upload_to='ticket_images/', blank=True, null=True, validators=[validate_image])
    image3 = models.ImageField(upload_to='ticket_images/', blank=True, null=True, validators=[validate_image])
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    is_visited = models.BooleanField(default=False)
    answer = models.TextField(blank=True, null=True)
    answered_time = jmodels.jDateTimeField(blank=True, null=True)
    created_time = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tickets'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if self.answer:
            gregorian_now = jdatetime.datetime.now().togregorian()
            aware_gregorian_now = timezone.make_aware(gregorian_now, timezone.get_current_timezone())
            self.answered_time = aware_gregorian_now
            self.status = 'answered'
        super().save(*args, **kwargs)
