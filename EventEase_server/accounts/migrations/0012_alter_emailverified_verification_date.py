# Generated by Django 5.0.6 on 2024-07-01 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_emailverified_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverified',
            name='verification_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]