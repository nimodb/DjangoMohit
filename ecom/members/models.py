from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from locations.models import *

VERIFICATION_CHOICES = [
    ("P", "Pending"),
    ("V", "Verified"),
    ("R", "Rejected"),
    ("I", "Incomplete"),
]


# Create your models here.
class Profile(AbstractUser):
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True
    )
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, blank=True, null=True
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    data_modified = models.DateTimeField(auto_now=True)
    verified = models.CharField(max_length=1, choices=VERIFICATION_CHOICES, default="I")

    def __str__(self):
        return self.username


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         user_profile = Profile(user=instance)
#         user_profile.save()


# post_save.connect(create_profile, sender=User)
