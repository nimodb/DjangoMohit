# Generated by Django 5.0.2 on 2024-03-19 06:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
