# Generated by Django 4.2 on 2024-09-02 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_source', '0002_financialsourcemodel_icon_color_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='financialsourcemodel',
            name='unique_account_card_number',
        ),
    ]
