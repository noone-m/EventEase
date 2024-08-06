# Generated by Django 5.0.6 on 2024-08-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_invitationcard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='other_type',
        ),
        migrations.AlterField(
            model_name='event',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
    ]