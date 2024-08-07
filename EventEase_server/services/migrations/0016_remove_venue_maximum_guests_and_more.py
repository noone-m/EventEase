# Generated by Django 5.0.6 on 2024-07-23 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_alter_djservice_area_limit_km_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='maximum_guests',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='minimum_guests',
        ),
        migrations.AlterField(
            model_name='decorationservice',
            name='area_limit_km',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entertainementservice',
            name='area_limit_km',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entertainementservice',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='photographerservice',
            name='area_limit_km',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='photographerservice',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='amenities',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='capacity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
