import django_filters
from django import forms
from store.models import Product, GENDER_CHOICES


class CustomPriceRangeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(attrs={"class": "form-control", "placeholder": "Min"}),
            forms.TextInput(attrs={"class": "form-control", "placeholder": "Max"}),
        )
        super().__init__(widgets, attrs)


class ProductFilter(django_filters.FilterSet):
    gender = django_filters.MultipleChoiceFilter(
        choices=GENDER_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
    )
    price = django_filters.RangeFilter(
        field_name="price",
        widget=CustomPriceRangeWidget(),
    )

    class Meta:
        model = Product
        fields = ["gender", "price"]
