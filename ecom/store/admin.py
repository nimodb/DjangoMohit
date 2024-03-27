from django.db.models import Count
from django.contrib import admin
from store.models import *


# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "breeds_count")
    readonly_fields = ("slug",)
    search_fields = ("name",)

    @admin.display(ordering="breeds_count")
    def breeds_count(self, group):
        return group.breeds_count

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                breeds_count=Count("breed"),
            )
        )


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "group")
    readonly_fields = ("slug",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "breed", "creator", "status")
    readonly_fields = ("timestamp", "modified_at")
    autocomplete_fields = ["breed"]


@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "product")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "status", "created_at")
    list_filter = ("status",)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "review")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rating")
