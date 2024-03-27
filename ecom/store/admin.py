from django.utils.html import format_html
from django.contrib import admin
from store.models import *


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "see_more_link",
        "custom_breed",
        "custom_price",
        "custom_status",
        "creator",
        "timestamp",
    )
    list_filter = ("status", "timestamp")
    search_fields = ["id", "group__name", "breed__name"]
    readonly_fields = ("timestamp", "modified_at")

    def see_more_link(self, obj):
        product_id = obj.id
        see_more_url = reverse("admin:store_product_change", args=[product_id])
        return format_html('<a href="{}">See More</a>', see_more_url)

    def custom_price(self, obj):
        if obj.price == 0 or obj.pct_price == 100:
            custom_p = "Free"
            return format_html(f"<span><b style='color: red;'>{custom_p}</b></span>")
        else:
            final_price = obj.price * (1 - obj.pct_price / 100)
            custom_p = "${:,.2f}".format(final_price)
            return format_html(
                f"<span><b>{custom_p}</b> <s>${obj.price}</s> (<small>%{obj.pct_price}</small>)</span>"
            )

    def custom_status(self, obj):
        if obj.status == "P":
            return format_html('<b style="color: blue;">Pending</b>')
        elif obj.status == "RE":
            return format_html('<b style="color: orange;">Revision</b>')
        elif obj.status == "A":
            return format_html('<b style="color: green;">Approved</b>')
        elif obj.status == "R":
            return format_html('<b style="color: red;">Rejected</b>')
        else:
            return obj.get_status_display()

    def custom_breed(self, obj):
        return format_html(
            f"<span><b>{obj.breed}</b> (<small>{obj.group}</small>)</span>"
        )

    custom_status.short_description = "Status"
    custom_breed.short_description = "Breed"
    custom_price.short_description = "Price"
    see_more_link.short_description = "See More"


class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "subject", "created_at", "custom_status")
    list_filter = ("status", "created_at")
    search_fields = ["id", "name", "email", "subject"]
    readonly_fields = ("created_at",)

    def custom_status(self, obj):
        if obj.status == "N":
            return format_html('<b style="color: blue;">New</b>')
        elif obj.status == "P":
            return format_html('<b style="color: green;">Awaiting Response</b>')
        elif obj.status == "R":
            return format_html('<b style="color: orange;">Response Sent</b>')

    custom_status.short_description = "Status"


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 0
    readonly_fields = ("created_at",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "see_more_link",
        "product_link",
        "rating",
        "created_at",
    )
    list_filter = ("created_at", "rating")
    search_fields = [
        "id",
        "product__group__name",
        "product__breed__name",
        "user__user__username",
    ]
    readonly_fields = ("created_at",)
    inlines = [ReplyInline]

    def see_more_link(self, obj):
        review_id = obj.id
        see_more_url = reverse("admin:store_review_change", args=[review_id])
        return format_html('<a href="{}">See Review</a>', see_more_url)

    def product_link(self, obj):
        product_id = obj.product.id
        product_url = reverse("admin:store_product_change", args=[product_id])
        return format_html('<a href="{}">See Product</a>', product_url, obj.product)

    product_link.short_description = "Product"


admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Review, ReviewAdmin)
