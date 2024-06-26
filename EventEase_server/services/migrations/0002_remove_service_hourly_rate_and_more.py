# Generated by Django 5.0.6 on 2024-05-24 12:54

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='hourly_rate',
        ),
        migrations.RemoveField(
            model_name='service',
            name='area_limit_km',
        ),
        migrations.CreateModel(
            name='FoodService',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='services.service')),
                ('cuisine_type', models.CharField(max_length=255)),
                ('menu', models.TextField()),
            ],
            bases=('services.service',),
        ),
        migrations.RenameField(
            model_name='serviceproviderapplication',
            old_name='serviceType',
            new_name='service_type',
        ),
        migrations.AddField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.location'),
        ),
        migrations.AddField(
            model_name='service',
            name='phone',
            field=models.CharField(default=None, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='serviceproviderapplication',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='serviceproviderapplication',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serviceproviderapplication',
            name='phone',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.servicetype'),
        ),
        migrations.AlterField(
            model_name='serviceproviderapplication',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.location'),
        ),
        migrations.AlterField(
            model_name='serviceproviderapplication',
            name='otherType',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='DJService',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='services.service')),
                ('music_genre', models.CharField(max_length=255)),
                ('equipment_provided', models.TextField()),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('area_limit_km', models.IntegerField()),
            ],
            bases=('services.service',),
        ),
    ]
