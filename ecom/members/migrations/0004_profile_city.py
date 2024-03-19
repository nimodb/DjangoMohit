# Generated by Django 5.0.2 on 2024-03-07 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_alter_state_country'),
        ('members', '0003_profile_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.city'),
        ),
    ]
