# Generated by Django 5.0.6 on 2024-08-04 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0007_remove_wallet_user_remove_centerwallet_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit'), ('transfer', 'Transfer')], max_length=15),
        ),
    ]
