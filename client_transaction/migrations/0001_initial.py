# Generated by Django 4.2 on 2024-09-03 01:41

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_source', '0003_remove_financialsourcemodel_unique_account_card_number'),
        ('client_category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('Income', 'Income'), ('Expense', 'Expense')], max_length=8)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=16)),
                ('transaction_level', models.CharField(blank=True, choices=[('Normal', 'Normal Transaction'), ('Unnecessary', 'Unnecessary Transaction')], max_length=11, null=True)),
                ('is_fee', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True)),
                ('created_time', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='client_category.categorymodel', verbose_name='category')),
                ('source', models.ForeignKey(error_messages='منبع مالی برای ثبت تراکنش الزامی است.', on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='client_source.financialsourcemodel', verbose_name='source')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'transactions',
            },
        ),
    ]
