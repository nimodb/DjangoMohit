from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)

from django.contrib.auth.models import User
from members.models import Profile
from store.models import Product, Group, Breed, ProductPhoto, ProductVideo
from members.models import Country, State, District, City
from dynamic_forms import DynamicField, DynamicFormMixin


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class InfoUserForm(DynamicFormMixin, forms.ModelForm):
    def state_choice(form):
        country = form["country"].value()
        if country:
            return State.objects.filter(country=country)
        return State.objects.none()

    def initial_state(form):
        country = form["country"].value()
        if country:
            return State.objects.filter(country=country).first()
        return None

    def district_choice(form):
        state = form["state"].value()
        if state:
            return District.objects.filter(state=state)
        return District.objects.none()

    def initial_district(form):
        state = form["state"].value()
        if state:
            return District.objects.filter(state=state).first()
        return None

    def city_choice(form):
        district = form["district"].value()
        if district:
            return City.objects.filter(district=district)
        return City.objects.none()

    def initial_city(form):
        district = form["district"].value()
        if district:
            return City.objects.filter(district=district).first()
        return None

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        initial=Country.objects.first(),
        required=False,
    )
    state = DynamicField(
        forms.ModelChoiceField,
        queryset=state_choice,
        initial=initial_state,
        required=False,
    )
    district = DynamicField(
        forms.ModelChoiceField,
        queryset=district_choice,
        initial=initial_district,
        required=False,
    )
    city = DynamicField(
        forms.ModelChoiceField,
        queryset=city_choice,
        initial=initial_city,
        required=False,
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial="IN"))

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "state",
            "district",
            "city",
        ]


class UpdateUserForm(UserChangeForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class ProductForm(DynamicFormMixin, forms.ModelForm):
    def breed_choice(form):
        group = form["group"].value()
        return Breed.objects.filter(group=group)

    def breed_initial(form):
        group = form["group"].value()
        return Breed.objects.filter(group=group).first()

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        initial=Group.objects.first(),
    )

    breed = DynamicField(
        forms.ModelChoiceField,
        queryset=breed_choice,
        initial=breed_initial,
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    class Meta:
        model = Product
        fields = [
            "group",
            "breed",
            "birthdate",
            "price",
            "pct_price",
            "summary",
            "description",
            "male_inventory",
            "female_inventory",
        ]
        widgets = {
            "price": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "pct_price": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class ProductPhotoForm(forms.ModelForm):
    class Meta:
        model = ProductPhoto
        fields = [
            "first_photo",
            "second_photo",
            "third_photo",
            "fourth_photo",
            "fifth_photo",
            "sixth_photo",
        ]


class ProductVideoForm(forms.ModelForm):
    class Meta:
        model = ProductVideo
        fields = [
            "first_video",
            "second_video",
        ]
