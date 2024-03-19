from datetime import timedelta, datetime
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)

ORDER_STATUS_CHOICES = (
    ("P", "Pending"),
    ("D", "Draft"),
    ("A", "Approved"),
    ("R", "Rejected"),
    ("I", "Inactive"),
    ("Ar", "Archived"),
)

ADMIN_STATUS_CHOICES = (
    ("P", "Pending"),
    ("RE", "Revision"),
    ("A", "Approved"),
    ("R", "Rejected"),
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("B", "Both"),
    ("N", "Not specified"),
)

IMG_EXT_VALIDATOR = FileExtensionValidator(
    ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "tif"]
)

VIDEO_EXT_VALIDATOR = FileExtensionValidator(
    ["mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"]
)


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="uploads/group/",
        help_text="Width: 1170px | Height: 500px",
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=1000, default="", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Breed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to="uploads/breed/",
        help_text="Width: 1170px | Height: 500px",
        null=True,
        blank=True,
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Breed, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, null=True, blank=True)
    birthdate = models.DateField(
        default=timezone.now, help_text="Birth date of the dog"
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        default=0,
        validators=[MinValueValidator(0)],
    )
    pct_price = models.DecimalField(
        decimal_places=0,
        max_digits=3,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    summary = models.TextField(max_length=145, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=ADMIN_STATUS_CHOICES, default="P")
    male_inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    female_inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def average_rating(self):
        avg_rating = self.reviews.aggregate(models.Avg("rating"))["rating__avg"]
        html = ""
        if avg_rating:
            full_stars = int(avg_rating)
            half_star = avg_rating - full_stars >= 0.5
            empty_stars = 5 - full_stars - (1 if half_star else 0)
            for _ in range(full_stars):
                html += '<i class="la la-star"></i>'
            if half_star:
                html += '<i class="la la-star-half-o"></i>'
            for _ in range(empty_stars):
                html += '<i class="la la-star-o"></i>'
            return html, avg_rating

    def product_last_week(self):
        return self.timestamp >= timezone.now() - timedelta(days=7)

    def product_last_day(self):
        return self.timestamp >= timezone.now() - timedelta(hours=12)

    def format_price(self):
        return "${:,.2f}".format(self.price)

    def format_pct_price(self):
        return f"{self.pct_price}%"

    def cal_price(self):
        if self.price == 0 or self.pct_price == 100:
            return 0
        else:
            final_price = self.price * (1 - self.pct_price / 100)
            return "${:,.2f}".format(final_price)

    def get_age(self):
        today = datetime.now()
        born = self.birthdate.strftime("%B %d, %Y")
        target_date = datetime.strptime(born, "%B %d, %Y")
        difference = today - target_date
        years = difference.days // 365
        months = (difference.days % 365) // 30
        days = (difference.days % 365) % 30
        if years == 0 and months == 0:
            return f"{days} day{'s' if days > 1 else ''}"
        elif years == 0:
            return f"{months} month{'s' if months > 1 else ''}, {days} day{'s' if days > 1 else ''}"
        elif months == 0:
            return f"{years} year{'s' if years > 1 else ''}"
        else:
            return f"{years} year{'s' if years > 1 else ''}, {months} month{'s' if months > 1 else ''}"


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="photos"
    )
    first_photo = models.ImageField(
        upload_to="uploads/product_images/",
        null=True,
        blank=True,
        validators=[IMG_EXT_VALIDATOR],
    )
    second_photo = models.ImageField(
        upload_to="uploads/product_images/",
        null=True,
        blank=True,
        validators=[IMG_EXT_VALIDATOR],
    )
    third_photo = models.ImageField(
        upload_to="uploads/product_images/",
        null=True,
        blank=True,
        validators=[IMG_EXT_VALIDATOR],
    )
    fourth_photo = models.ImageField(
        upload_to="uploads/product_images/",
        null=True,
        blank=True,
        validators=[IMG_EXT_VALIDATOR],
    )
    fifth_photo = models.ImageField(
        upload_to="uploads/product_images/",
        null=True,
        blank=True,
        validators=[IMG_EXT_VALIDATOR],
    )
    sixth_photo = models.ImageField(
        upload_to="uploads/product_images/",
        null=True,
        blank=True,
        validators=[IMG_EXT_VALIDATOR],
    )


class ProductVideo(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="Videos"
    )
    first_video = models.FileField(
        upload_to="uploads/product_videos/",
        null=True,
        blank=True,
        validators=[VIDEO_EXT_VALIDATOR],
    )
    second_video = models.FileField(
        upload_to="uploads/product_videos/",
        null=True,
        blank=True,
        validators=[VIDEO_EXT_VALIDATOR],
    )
