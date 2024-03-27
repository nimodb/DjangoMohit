from django.contrib import admin
from .models import Profile


# Register your models here
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "phone",
        "country",
        "state",
        "district",
        "city",
        "verified",
        "data_modified",
    ]
    search_fields = ["username", "phone", "country", "state", "district", "city"]
    list_filter = ["verified"]
    fieldsets = (
        (
            "User Information",
            {
                "fields": ("username", "phone"),
            },
        ),
        (
            "Location",
            {
                "fields": ("country", "state", "district", "city"),
            },
        ),
        (
            "Verification Status",
            {
                "fields": ("verified",),
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        (
            "Metadata",
            {
                "fields": ("data_modified", "date_joined"),
            },
        ),
    )
    readonly_fields = ["data_modified", "date_joined"]
