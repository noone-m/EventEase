# Generated by Django 5.0.6 on 2024-05-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_remove_foodservice_cuisine_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='gradients',
            field=models.TextField(null=True),
        ),
    ]
