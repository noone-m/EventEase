# Generated by Django 5.0.6 on 2024-07-23 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0016_remove_venue_maximum_guests_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetype',
            name='type',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]