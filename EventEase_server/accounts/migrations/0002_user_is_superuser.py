# Generated by Django 5.0.6 on 2024-05-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates whether the user is super user or not.', verbose_name='super user status'),
        ),
    ]
