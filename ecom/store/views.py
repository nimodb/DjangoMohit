from ipware import get_client_ip
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Min, Max
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from store.models import *
from store.filters import ProductFilter
from store.forms import ReviewForm, ReplyForm
from members.models import Review, Wishlist


# Create your views here.
def navigation_bar_group():
    groups = Group.objects.all()
    navigation_bar = {}
    for group in groups:
        group_name = group.name
        group_slug = group.slug
        breeds = Breed.objects.filter(group=group)

        breed_data = []
        for breed in breeds[:5]:
            breed_data.append(
                {
                    "name": breed.name,
                    "slug": breed.slug,
                }
            )
        navigation_bar[group_name] = {
            "breeds": breed_data,
            "group_slug": group_slug,
            "breeds_count": (breeds.count() - 5),
        }
    return navigation_bar


def create_context(request):
    groups_navbar = navigation_bar_group()
    current_year = datetime.now().year
    favorites_count = 0
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            favorites_count = wishlist.products.count()
    context = {
        "groups_navbar": groups_navbar,
        "favorite_count": favorites_count,
        "current_year": current_year,
    }
    return context


def home(request):
    context = create_context(request)
    products = Product.objects.order_by("-timestamp")[:20]
    top_discounts = Product.objects.filter(
        pct_price__gt=0, pct_price__lt=100, price__gt=0
    ).order_by("-pct_price")[:20]

    context["products"] = products
    context["top_discounts"] = top_discounts
    return render(request, "index.html", context)


def contact(request):
    context = create_context(request)
    return render(request, "contact.html", context)


def search(request):
    context = create_context(request)
    return render(request, "search.html", context)


def groups(request):
    context = create_context(request)
    query = request.GET.get("query")
    if query:
        context["query"] = query
        groups = Group.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        if not groups:
            messages.error(request, "No groups found")
    else:
        groups = Group.objects.all()

    paginator = Paginator(groups, 5)
    page = request.GET.get("page")
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    navigation_bar = navigation_bar_group()
    context["navigation_bar"] = navigation_bar
    context["groups"] = groups
    return render(request, "group-list.html", context)


def search_by_breeds(request):
    gender_m = request.POST.get("gender_m")
    gender_f = request.POST.get("gender_f")
    search_breed = request.POST.get("search_breed")
    min_price = request.POST.get("min_price")
    max_price = request.POST.get("max_price")

    breed_filter = Q()
    if search_breed:
        breed_filter |= Q(breed__name__icontains=search_breed.lower())

    gender_filter = Q()
    if gender_m:
        gender_filter |= Q(male_inventory__gte=1)
    if gender_f:
        gender_filter |= Q(female_inventory__gte=1)

    price_filter = Q()
    if min_price:
        price_filter &= Q(price__gte=min_price)
    if max_price:
        price_filter &= Q(price__lte=max_price)

    combined_filter = gender_filter & breed_filter & price_filter

    products = Product.objects.filter(combined_filter)
    paginator = Paginator(products, 100)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {"products": products}

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_products_ids = list(wishlist.products.values_list("id", flat=True))
            context["wishlist"] = wishlist_products_ids
    return render(request, "partials/hx/search_product.html", context)


def search_product(request, slug):
    group_slug = slug
    search_text = request.POST.get("search")
    if search_text:
        search_text = search_text.lower()
        products = (
            Product.objects.filter(group__slug=group_slug)
            .filter(
                Q(name__icontains=search_text) | Q(description__icontains=search_text)
            )
            .distinct()
        )
    else:
        products = Product.objects.filter(group__slug=group_slug)
    paginator = Paginator(products, 100)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {"products": products}

    return render(request, "partials/hx/search_product.html", context)


def group_detail(request, slug):
    context = create_context(request)
    gender_choices = GENDER_CHOICES
    group = get_object_or_404(Group, slug=slug)
    breeds = Breed.objects.filter(group=group).annotate(
        product_count=models.Count("product")
    )
    product_filter = ProductFilter(
        request.GET, queryset=Product.objects.filter(group=group)
    )
    form = product_filter.form
    products = product_filter.qs
    if products.exists():
        min_max_price = products.aggregate(Min("price"), Max("price"))
    else:
        min_max_price = None

    paginator = Paginator(products, 5)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context["group"] = group
    context["breeds"] = breeds
    context["products"] = products
    context["form"] = form
    context["min_max_price"] = min_max_price
    context["gender_choices"] = gender_choices
    context["selected_genders"] = form.data.getlist("gender")
    return render(request, "group-details.html", context)


def breeds(request):
    context = create_context(request)
    query = request.GET.get("query")
    if query:
        context["query"] = query
        groups = Group.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        if not groups:
            messages.error(request, "No groups found")
    else:
        groups = Group.objects.all()

    paginator = Paginator(groups, 5)
    page = request.GET.get("page")
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    navigation_bar = navigation_bar_group()
    context["navigation_bar"] = navigation_bar
    context["groups"] = groups
    return render(request, "group-list.html", context)


def breed_detail(request, slug):
    breed = get_object_or_404(Breed, slug=slug)
    products = Product.objects.filter(breed=breed)
    context = create_context(request)
    context["breed"] = breed
    context["products"] = products
    return render(request, "breed-details.html", context)


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
            return redirect("store:product", pk=review.product.pk)
        else:
            for error in list(reply_form.errors.values()):
                messages.error(request, error)
    return redirect("store:product", pk=review.product.pk)


def search_puppies(request):
    context = create_context(request)
    products = Product.objects.all()
    breeds = Breed.objects.all()
    paginator = Paginator(products, 100)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_products_ids = list(wishlist.products.values_list("id", flat=True))
            context["wishlist"] = wishlist_products_ids

    context["products"] = products
    context["breeds"] = breeds
    return render(request, "store/search-puppies.html", context)


def product(request, pk):
    context = create_context(request)
    product = get_object_or_404(Product, pk=pk)
    products = Product.objects.filter(group=product.group).order_by("-modified_at")[:10]

    if request.user.is_authenticated:
        if request.method == "POST":
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(
                    request, "Your review has been submitted successfully."
                )
                return redirect("store:product", pk=product.pk)
            else:
                for error in list(review_form.errors.values()):
                    messages.error(request, error)
        else:
            is_owner = True if request.user == product.creator else False
            review_form = ReviewForm()
            reply_form = ReplyForm()
            context["review_form"] = review_form
            context["reply_form"] = reply_form
            context["is_owner"] = is_owner

    context["product"] = product
    context["products"] = products
    return render(request, "store/product-details-tab1.html", context)
