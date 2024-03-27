import datetime
from django.http.response import HttpResponse
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms.models import model_to_dict
from django.contrib.auth import (
    login,
    logout,
    authenticate,
    update_session_auth_hash,
    get_user_model,
)

# from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from members.forms import (
    LoginForm,
    RegistrationForm,
    UpdateUserForm,
    InfoUserForm,
    ProductForm,
    ProductPhotoForm,
    ProductVideoForm,
)
from members.models import Profile
from store.models import Product, ProductPhoto, ProductVideo, Wishlist, Review
from store.views import create_context
from store.forms import ReviewForm, ReplyForm


# Create your views here.
def convert_to_readable_time(data):
    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    return data


def login_user(request):
    if request.user.is_authenticated:
        return redirect("members:dashboard")

    context = create_context(request)
    login_form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "You have been successfully logged in.")
                return redirect("members:dashboard")
            else:
                messages.warning(request, "Invalid username or password.")
        else:
            for error in list(login_form.errors.values()):
                messages.warning(request, error)

    context["login_form"] = login_form
    return render(request, "members/login.html", context=context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect("members:dashboard")
    context = create_context(request)
    registration_form = RegistrationForm()

    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            username = registration_form.cleaned_data.get("username")
            if get_user_model().objects.filter(username=username).exists():
                registration_form.add_error("username", "Username is already taken.")
            else:
                registration_form.save()
                password = registration_form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "Success! Your registration is complete.")
                return redirect("members:dashboard")

        else:
            for error in list(registration_form.errors.values()):
                messages.warning(request, error)

    context["registration_form"] = registration_form
    return render(request, "members/register.html", context=context)


def profile_has_changed(profile, old_profile_data):
    # Compare each field of the profile with the old profile data
    for field, value in old_profile_data.items():
        if field not in ["_state", "id", "user"]:  # Exclude non-field attributes
            if getattr(profile, field) != value:
                return True  # Field has changed
    return False  # No field has changed


def submit_reply(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.review = review
            reply.user = request.user
            reply.save()
            messages.success(request, "Your reply has been submitted successfully.")
            return redirect("members:list_posts")
        else:
            for error in list(reply_form.errors.values()):
                messages.error(request, error)
    return redirect("members:list_posts")


def list_posts(request):
    if not request.user.is_authenticated:
        return redirect("members:login")

    if request.user.verified != "V":
        messages.warning(
            request,
            "Your profile is pending verification (Please wait for our team to review it.)",
        )
        return redirect("members:dashboard")

    context = create_context(request)
    current_user = request.user
    products = (
        Product.objects.filter(creator_id=current_user.id)
        .order_by("status")
        .order_by("-modified_at")
    )
    review_form = ReviewForm()
    reply_form = ReplyForm()
    wishlist_products_ids = Wishlist.objects.values_list("products", flat=True)
    products_count = dict(Counter(wishlist_products_ids))

    context["products"] = products
    context["review_form"] = review_form
    context["reply_form"] = reply_form
    context["products_count"] = products_count
    return render(request, "members/list-posts.html", context)


def account_details(request):
    if not request.user.is_authenticated:
        return redirect("members:login")
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "phone",
        "country",
        "state",
        "district",
        "city",
        "verified",
    ]
    user_data_before = model_to_dict(request.user, fields=fields)
    if request.method == "POST":
        form = InfoUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            user_data_after = model_to_dict(request.user, fields=fields)

            user_changed = user_data_before != user_data_after
            if user_changed:
                empty_info = any(
                    value == "" or value == None for value in user_data_after.values()
                )
                request.user.verified = "I" if empty_info else "P"
                request.user.save(update_fields=["verified"])

                message = (
                    "Please ensure all required fields are filled out before saving changes."
                    if empty_info
                    else "Your details have been updated. Changes are pending review."
                )
                if empty_info:
                    messages.warning(request, message)
                else:
                    messages.success(request, message)
            else:
                messages.info(request, "No changes detected.")
            return redirect("members:account_details")
        else:
            for error in list(form.errors.values()):
                messages.warning(request, error)
            return redirect("members:account_details")
    else:
        form = InfoUserForm(instance=request.user)
    context = create_context(request)
    context["form"] = form
    return render(request, "members/account-details.html", context)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("members:login")

    context = create_context(request)
    current_user = request.user
    products = Product.objects.filter(creator_id=current_user.id).order_by("status")
    context["products"] = products
    return render(request, "members/my-account.html", context)


def wishlist(request):
    if not request.user.is_authenticated:
        return redirect("members:login")
    context = create_context(request)
    wishlist = Wishlist.objects.filter(user=request.user).first()
    context["wishlist"] = wishlist
    return render(request, "members/wishlist.html", context)


def add_to_wishlist(request, pk):
    product = Product.objects.get(pk=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return HttpResponse("<i class='fa-solid fa-heart-circle-check text-danger'></i>")


def remove_from_wishlist(request, pk):
    if not request.user.is_authenticated:
        return redirect("members:login")
    if request.user.verified != "V":
        messages.warning(
            request,
            "Your profile is pending verification (Please wait for our team to review it.)",
        )
        return redirect("members:dashboard")

    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.products.remove(product)
        messages.success(request, "Your Post have been Removed.")
        return redirect("members:wishlist")
    else:
        return redirect("members:wishlist")


def delete_post(request, pk):
    if not request.user.is_authenticated:
        return redirect("members:login")
    if request.user.verified != "V":
        messages.warning(
            request,
            "Your profile is pending verification (Please wait for our team to review it.)",
        )
        return redirect("members:dashboard")

    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)
        print(product)
        product.delete()
        messages.success(request, "Your Post have been Deleted.")
        return redirect("members:list_posts")
    else:
        return redirect("members:list_posts")


def edit_post(request, pk):
    if not request.user.is_authenticated:
        return redirect("members:login")
    if request.user.verified != "V":
        messages.warning(
            request,
            "Your profile is pending verification (Please wait for our team to review it.)",
        )
        return redirect("members:dashboard")

    product = get_object_or_404(Product, pk=pk)
    photo_instance = get_object_or_404(ProductPhoto, product=product)
    video_instance = get_object_or_404(ProductVideo, product=product)
    xxxx_data_before = model_to_dict(product, exclude=["summary", "description"])
    product_data_before = model_to_dict(product, fields=["summary", "description"])
    photo_instance_data_before = model_to_dict(photo_instance)
    video_instance_data_before = model_to_dict(video_instance)
    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product)
        photo_form = ProductPhotoForm(
            request.POST, request.FILES, instance=photo_instance
        )
        video_form = ProductVideoForm(
            request.POST, request.FILES, instance=video_instance
        )
        if product_form.is_valid() and photo_form.is_valid() and video_form.is_valid():
            product = product_form.save(commit=False)
            product.save()
            photo = photo_form.save(commit=False)
            photo.product = product
            photo.save()
            video = video_form.save(commit=False)
            video.product = product
            video.save()

            xxxx_data_after = model_to_dict(product, exclude=["summary", "description"])
            product_data_after = model_to_dict(
                product, fields=["summary", "description"]
            )
            photo_instance_data_after = model_to_dict(photo_instance)
            video_instance_data_after = model_to_dict(video_instance)

            xxxx_changed = xxxx_data_before != xxxx_data_after
            product_changed = product_data_before != product_data_after
            photo_instance_changed = (
                photo_instance_data_before != photo_instance_data_after
            )
            video_instance_changed = (
                video_instance_data_before != video_instance_data_after
            )
            if product_changed or photo_instance_changed or video_instance_changed:
                product.status = "P"
                product.save()
                messages.success(
                    request,
                    "Post updated successfully. We'll review and update status soon.",
                )
            elif xxxx_changed:
                messages.success(request, "Post updated successfully.")
            else:
                messages.info(request, "No changes detected.")
            return redirect("members:list_posts")
        else:
            for form in [product_form, photo_form, video_form]:
                for error in list(form.errors.values()):
                    messages.warning(request, error)
            return redirect("members:list_posts")
    else:
        product_form = ProductForm(instance=product)
        photo_form = ProductPhotoForm(instance=photo_instance)
        video_form = ProductVideoForm(instance=video_instance)
    context = create_context(request)
    context.update(
        {
            "product": product,
            "product_form": product_form,
            "photo_form": photo_form,
            "video_form": video_form,
        }
    )
    return render(request, "members/edit-post.html", context)


def add_post(request):
    if not request.user.is_authenticated:
        return redirect("members:login")
    if request.user.verified != "V":
        messages.warning(
            request,
            "Your profile is pending verification (Please wait for our team to review it.)",
        )
        return redirect("members:dashboard")

    context = create_context(request)
    current_user = request.user
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        photo_form = ProductPhotoForm(request.POST, request.FILES)
        video_form = ProductVideoForm(request.POST, request.FILES)
        if product_form.is_valid() and photo_form.is_valid() and video_form.is_valid():
            product = product_form.save(commit=False)
            product.creator = current_user
            product.save()
            photo = photo_form.save(commit=False)
            photo.product = product
            photo.save()
            video = video_form.save(commit=False)
            video.product = product
            video.save()
            messages.success(
                request,
                "Post submitted successfully. We'll review and update status soon.",
            )
            return redirect("members:list_posts")
        else:
            for error in list(product_form.errors.values()):
                messages.warning(request, error)
            for error in list(photo_form.errors.values()):
                messages.warning(request, error)
            for error in list(video_form.errors.values()):
                messages.warning(request, error)
            return redirect("members:list_posts")
    else:
        product_form = ProductForm()
        photo_form = ProductPhotoForm()
        video_form = ProductVideoForm()
    context["product_form"] = product_form
    context["photo_form"] = photo_form
    context["video_form"] = video_form
    return render(request, "members/add-post.html", context)


def update_password(request):
    if not request.user.is_authenticated:
        return redirect("members:login")

    current_user = request.user
    context = create_context(request)
    if request.method == "POST":
        password_form = PasswordChangeForm(current_user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed.")
            return redirect("members:account_details")
        else:
            for error in list(password_form.errors.values()):
                messages.warning(request, error)
            return redirect("members:update_password")
    else:
        password_form = PasswordChangeForm(current_user)

    context["password_form"] = password_form

    return render(request, "members/update-password.html", context)


def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("store:home")


def check_username_register(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse(
            "<div class='text-danger mt-2'>This username already exists</div>"
        )
    else:
        return HttpResponse(
            "<div class='text-success mt-2'>This username is available</div>"
        )


def check_username_login(request):
    username = request.POST.get("username")
    if username != "":
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse("")
        else:
            return HttpResponse(
                "<div class='text-danger mt-2'>This username not exists</div>"
            )
    else:
        return HttpResponse("")


def check_email(request):
    email = request.POST.get("email")
    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse(
            "<div class='text-danger mt-2'>This email address already exists</div>"
        )
    else:
        return HttpResponse("")


def check_breed(request):
    form = ProductForm(request.GET)
    return HttpResponse(form["breed"])


def check_state(request):
    form = InfoUserForm(request.GET)
    return HttpResponse(form["state"])


def check_district(request):
    form = InfoUserForm(request.GET)
    return HttpResponse(form["district"])


def check_city(request):
    form = InfoUserForm(request.GET)
    return HttpResponse(form["city"])
