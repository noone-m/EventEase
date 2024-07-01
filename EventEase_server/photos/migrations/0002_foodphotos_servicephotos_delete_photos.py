# Generated by Django 5.0.6 on 2024-05-29 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
        ('services', '0004_remove_foodservice_cuisine_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.ImageField(upload_to='food/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.food')),
            ],
        ),
        migrations.CreateModel(
            name='ServicePhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.ImageField(upload_to='services/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
            ],
        ),
        migrations.DeleteModel(
            name='Photos',
        ),
    ]