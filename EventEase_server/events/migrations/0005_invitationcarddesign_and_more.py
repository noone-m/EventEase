# Generated by Django 5.0.6 on 2024-08-16 06:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_event_other_type_alter_event_total_cost_and_more'),
        ('locations', '0004_alter_address_country_alter_address_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationCardDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pictures/card_design')),
                ('image_width', models.IntegerField()),
                ('image_hieght', models.IntegerField()),
                ('width', models.IntegerField()),
                ('hight', models.IntegerField()),
                ('start_x', models.IntegerField()),
                ('start_y', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='invitationcard',
            old_name='invitation',
            new_name='text',
        ),
        migrations.AddField(
            model_name='invitationcard',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.location'),
        ),
        migrations.AddField(
            model_name='invitationcard',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
