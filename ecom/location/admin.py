from django.contrib import admin
from .models import Country, State, District, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = ["name"]
    list_display = ("name",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = ["name"]
    list_display = ("name", "country")
    autocomplete_fields = ["country"]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = ["name"]
    list_display = ("name", "state")
    autocomplete_fields = ["state"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = ["name"]
    list_display = ("name", "district")
    autocomplete_fields = ["district"]
