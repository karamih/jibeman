# Generated by Django 4.2 on 2024-07-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('Free', 'Free'), ('Standard', 'Standard'), ('Premium', 'Premium')], default='Free', max_length=8)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('duration_month', models.PositiveIntegerField(choices=[(1, '1 Month'), (3, '3 Months'), (6, '6 Months'), (12, '12 Months')], default=1)),
            ],
            options={
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
                'db_table': 'subscription',
            },
        ),
    ]
