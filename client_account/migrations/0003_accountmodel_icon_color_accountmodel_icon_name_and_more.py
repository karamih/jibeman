# Generated by Django 4.2 on 2024-08-16 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_account', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountmodel',
            name='icon_color',
            field=models.CharField(default='ffffff', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='icon_name',
            field=models.CharField(default='home', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountmodel',
            name='credit',
            field=models.IntegerField(default=0),
        ),
    ]
