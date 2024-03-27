from datetime import timedelta, datetime
from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from telegram import Bot, InputMediaPhoto
from telegram.constants import ParseMode
from urllib.parse import urljoin
import asyncio
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)
from members.models import Profile

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

CONTACT_CHOICES = (
    ("N", "New"),
    ("P", "Awaiting Response"),
    ("R", "Response Sent"),
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
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
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=ADMIN_STATUS_CHOICES, default="P")
    male_inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    female_inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def get_absolute_url(self):
        domain = settings.BASE_URL
        return f"{domain}{reverse('store:product', args=[self.pk])}"

    def save(self, *args, **kwargs):
        old_product_main = None
        old_product_desc = None
        if self.pk:
            old_product_main = model_to_dict(
                Product.objects.get(pk=self.pk), exclude=["summary", "description"]
            )
            old_product_desc = model_to_dict(
                Product.objects.get(pk=self.pk), fields=["summary", "description"]
            )
            old_photo_instance_data = model_to_dict(
                ProductPhoto.objects.get(product_id=self.pk)
            )
            old_video_instance_data = model_to_dict(
                ProductVideo.objects.get(product_id=self.pk)
            )
        super().save(*args, **kwargs)
        if self.pk and old_product_main and old_product_desc:
            new_product_main = model_to_dict(
                Product.objects.get(pk=self.pk), exclude=["summary", "description"]
            )
            new_product_desc = model_to_dict(
                Product.objects.get(pk=self.pk), fields=["summary", "description"]
            )
            new_photo_instance_data = model_to_dict(
                ProductPhoto.objects.get(product_id=self.pk)
            )
            new_video_instance_data = model_to_dict(
                ProductVideo.objects.get(product_id=self.pk)
            )
            changed_product_desc = new_product_desc != old_product_desc
            changed_product_main = new_product_main != old_product_main
            changed_photo_instance = old_photo_instance_data != new_photo_instance_data
            changed_video_instance = old_video_instance_data != new_video_instance_data
            if not (
                changed_product_desc
                and changed_video_instance
                and changed_photo_instance
            ):
                if changed_product_main:
                    if new_product_main["status"] == "A":
                        media_group = self.get_image_urls()
                        caption = self.generate_caption()
                        asyncio.run(self.telegram_message(media_group, caption))

    def get_full_media_url(self, relative_url):
        return urljoin(settings.BASE_URL, relative_url)

    def get_image_urls(self):
        video_urls = []
        # for video in self.videos.all():
        #     pass
        image_urls = []
        for photo in self.photos.all():
            image_data = {}
            image_data["first_photo"] = (
                self.get_full_media_url(photo.first_photo.url)
                if photo.first_photo
                else None
            )
            image_data["second_photo"] = (
                self.get_full_media_url(photo.second_photo.url)
                if photo.second_photo
                else None
            )
            image_data["third_photo"] = (
                self.get_full_media_url(photo.third_photo.url)
                if photo.third_photo
                else None
            )
            image_data["fourth_photo"] = (
                self.get_full_media_url(photo.fourth_photo.url)
                if photo.fourth_photo
                else None
            )
            image_data["fifth_photo"] = (
                self.get_full_media_url(photo.fifth_photo.url)
                if photo.fifth_photo
                else None
            )
            image_data["sixth_photo"] = (
                self.get_full_media_url(photo.sixth_photo.url)
                if photo.sixth_photo
                else None
            )
            image_urls.append(image_data)

        media_group = []
        for media in image_urls:
            for key, value in media.items():
                if value:
                    media_group.append(InputMediaPhoto(media=value))
        return media_group

    def generate_caption(self):
        caption = "<b>💫 Indian Dog Store</b>\n\n"
        caption += f"<b>Breed:</b> {self.group}, {self.breed}\n"

        gender_info = []
        if self.female_inventory:
            gender_info.append(f"Female: {self.female_inventory}")
        if self.male_inventory:
            gender_info.append(f"Male: {self.male_inventory}")
        if gender_info:
            caption += "<b>Gender:</b> " + ", ".join(gender_info) + "\n"

        caption += (
            f"<b>Age:</b> {self.get_age()} ({self.birthdate.strftime('%B %d, %Y')})\n"
        )

        if self.cal_price() == 0:
            caption += f"<b>Price:</b> 🆓FREE\n"
        else:
            caption += f"<b>Price:</b> {self.cal_price()}"
            if self.cal_price() != self.format_price:
                caption += f" <s>{self.format_price()}</s> (-{self.pct_price}%)\n"

        location_info = []
        if self.creator.city:
            location_info.append(f"{self.creator.city.name}")
        if self.creator.district:
            location_info.append(f"{self.creator.district.name}")
        if self.creator.state:
            location_info.append(f"{self.creator.state.name}")
        if self.creator.country:
            location_info.append(f"{self.creator.country.name}")
        if location_info:
            caption += "<b>Location:</b> " + ", ".join(location_info) + "\n"

        caption += f"\n\n<b>Phone:</b> {self.creator.phone}\n"
        caption += f"<b>Email:</b> {self.creator.email}\n\n"

        caption += f"<a href='{self.get_full_media_url(relative_url=reverse('store:product', args=[self.pk]))}'><b>See more</b></a>\n\n"
        return caption

    async def telegram_message(self, media_group, caption):
        bot_token = settings.TELEGRAM_BOT_TOKEN
        channel_id = settings.TELEGRAM_CHANNEL_ID
        bot = Bot(token=bot_token)
        caption = caption
        try:
            await bot.send_media_group(
                chat_id=channel_id,
                media=media_group,
                caption=caption,
                parse_mode=ParseMode.HTML,
            )
        except:
            await bot.send_message(
                chat_id=channel_id, text=caption, parse_mode=ParseMode.HTML
            )

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


class Wishlist(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Wishlist for {self.user.username}"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s review"


class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.review}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CONTACT_CHOICES, default="N")


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
