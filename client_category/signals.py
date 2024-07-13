from django.db.models.signals import post_save
from django.dispatch import receiver
from client_account.models import AccountModel
from admin_category.models import DefaultCategoryModel
from .models import CategoryModel


@receiver(post_save, sender=AccountModel)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = DefaultCategoryModel.objects.all()
        for cat in default_categories:
            CategoryModel.objects.create(
                account=instance,
                name=cat.name,
                transaction_type=cat.transaction_type,
                is_default=cat.is_default
            )
