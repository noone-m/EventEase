# Generated by Django 5.0.6 on 2024-07-16 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_alter_service_service_provider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decorationservice',
            name='hourly_rate',
        ),
        migrations.RemoveField(
            model_name='decore',
            name='photo',
        ),
    ]
