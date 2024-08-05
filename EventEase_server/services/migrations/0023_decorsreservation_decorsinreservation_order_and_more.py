# Generated by Django 5.0.6 on 2024-08-02 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_event_other_type_alter_event_total_cost_and_more'),
        ('services', '0022_service_avg_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecorsReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], max_length=20)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('decor_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.decorationservice')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='DecorsInReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('price', models.FloatField()),
                ('decor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.decor')),
                ('decors_reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.decorsreservation')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], max_length=20)),
                ('total_price', models.FloatField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
            ],
        ),
        migrations.CreateModel(
            name='FoodInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.order')),
            ],
        ),
        migrations.CreateModel(
            name='DecorInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('decor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.decor')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.order')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], max_length=20)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
            ],
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
