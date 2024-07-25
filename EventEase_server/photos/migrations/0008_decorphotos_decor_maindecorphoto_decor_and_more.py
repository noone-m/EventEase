# Generated by Django 5.0.6 on 2024-07-23 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0007_decorphotos_maindecorphoto'),
        ('services', '0018_remove_decoreventtype_decore_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='decorphotos',
            name='decor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.decor'),
        ),
        migrations.AddField(
            model_name='maindecorphoto',
            name='decor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.decor'),
        ),
        migrations.AddField(
            model_name='maindecorphoto',
            name='decorPhoto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.decorphotos'),
        ),
    ]