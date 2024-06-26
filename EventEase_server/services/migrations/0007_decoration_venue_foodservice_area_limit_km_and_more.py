# Generated by Django 5.0.6 on 2024-06-04 21:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_alter_address_country_alter_address_state_and_more'),
        ('services', '0006_rename_gradients_food_ingredients'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Decoration',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='services.service')),
            ],
            bases=('services.service',),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='services.service')),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('capacity', models.IntegerField()),
                ('amenities', models.TextField()),
                ('minimum_guests', models.IntegerField()),
                ('maximum_guests', models.IntegerField()),
            ],
            bases=('services.service',),
        ),
        migrations.AddField(
            model_name='foodservice',
            name='area_limit_km',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serviceproviderapplication',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serviceProviderApplication', to='locations.location'),
        ),
        migrations.AlterField(
            model_name='serviceproviderapplication',
            name='national_identity_back',
            field=models.ImageField(upload_to='storage/pictures/identity/'),
        ),
        migrations.AlterField(
            model_name='serviceproviderapplication',
            name='national_identity_front',
            field=models.ImageField(upload_to='storage/pictures/identity/'),
        ),
        migrations.AlterField(
            model_name='serviceproviderapplication',
            name='service_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='serviceType', to='services.servicetype'),
        ),
        migrations.AlterField(
            model_name='serviceproviderapplication',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
