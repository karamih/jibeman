# Generated by Django 4.2 on 2024-07-08 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("admin_notification", "0001_initial"),
        ("client_user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notificationmodel",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to="client_user.profilemodel",
                verbose_name="profile",
            ),
        ),
    ]
