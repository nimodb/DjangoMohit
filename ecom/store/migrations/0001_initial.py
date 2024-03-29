# Generated by Django 5.0.3 on 2024-03-23 20:04

import ckeditor.fields
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, help_text='Width: 1170px | Height: 500px', null=True, upload_to='uploads/group/')),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, help_text='Width: 1170px | Height: 500px', null=True, upload_to='uploads/breed/')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.group')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(default=django.utils.timezone.now, help_text='Birth date of the dog')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('pct_price', models.DecimalField(decimal_places=0, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('summary', models.TextField(blank=True, max_length=145, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('RE', 'Revision'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=10)),
                ('male_inventory', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('female_inventory', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('breed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.breed')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.group')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_photo', models.ImageField(blank=True, null=True, upload_to='uploads/product_images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'])])),
                ('second_photo', models.ImageField(blank=True, null=True, upload_to='uploads/product_images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'])])),
                ('third_photo', models.ImageField(blank=True, null=True, upload_to='uploads/product_images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'])])),
                ('fourth_photo', models.ImageField(blank=True, null=True, upload_to='uploads/product_images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'])])),
                ('fifth_photo', models.ImageField(blank=True, null=True, upload_to='uploads/product_images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'])])),
                ('sixth_photo', models.ImageField(blank=True, null=True, upload_to='uploads/product_images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'])])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_video', models.FileField(blank=True, null=True, upload_to='uploads/product_videos/', validators=[django.core.validators.FileExtensionValidator(['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm'])])),
                ('second_video', models.FileField(blank=True, null=True, upload_to='uploads/product_videos/', validators=[django.core.validators.FileExtensionValidator(['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm'])])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Videos', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='store.review')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('products', models.ManyToManyField(to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
