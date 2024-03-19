from django.urls import path
from store import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("contact/", views.contact, name="contact"),
    path("search-puppies/", views.search_puppies, name="search_puppies"),
    path("product/<int:pk>", views.product, name="product"),
    path("submit-reply/<int:pk>", views.submit_reply, name="submit_reply"),
    #
    path("groups/", views.groups, name="groups"),
    path("groups/<slug:slug>", views.group_detail, name="group_detail"),
    #
    path("breeds/", views.breeds, name="breeds"),
    path("breed/<slug:slug>", views.breed_detail, name="breed_detail"),
]

hmtx_views = [
    path("search-by-breeds/", views.search_by_breeds, name="search_by_breeds"),
    path(
        "groups/<slug:slug>/search-product/",
        views.search_product,
        name="search-product",
    ),
]


urlpatterns += hmtx_views
