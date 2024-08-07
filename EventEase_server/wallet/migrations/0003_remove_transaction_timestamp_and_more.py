# Generated by Django 5.0.6 on 2024-07-31 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_remove_wallet_currency_alter_wallet_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='wallet',
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_transactions', to='wallet.wallet'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_transactions', to='wallet.wallet'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit'), ('transfer', 'Transfer'), ('fee', 'Fee'), ('refund', 'Refund')], max_length=15),
        ),
    ]
