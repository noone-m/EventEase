# Generated by Django 5.0.6 on 2024-07-31 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportservice',
            name='evidence',
            field=models.FileField(blank=True, null=True, upload_to='reports/evidence/'),
        ),
    ]
