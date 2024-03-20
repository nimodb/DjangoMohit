from django.urls import path
from members import views

app_name = "members"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("update_password/", views.update_password, name="update_password"),
    path("logout/", views.logout_user, name="logout"),
    # account   
    path("dashboard/", views.dashboard, name="dashboard"),
    path("account-details/", views.account_details, name="account_details"),
    path("list_posts/", views.list_posts, name="list_posts"),
    path("submit-reply/<int:pk>", views.submit_reply, name="submit_reply"),
    # Post process
    path("add/", views.add_post, name="add_post"),
    path("edit/<int:pk>/", views.edit_post, name="edit_post"),
    path("delete/<int:pk>/", views.delete_post, name="delete_post"),
    # Wishlist
    path("wishlist/", views.wishlist, name="wishlist"),
    path(
        "remove_from_wishlist/<int:pk>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
]


hmtx_views = [
    path(
        "check-username-register/",
        views.check_username_register,
        name="check-username-register",
    ),
    path(
        "check-username-login/", views.check_username_login, name="check-username-login"
    ),
    path("check-email/", views.check_email, name="check-email"),
    path("check-breed/", views.check_breed, name="check-breed"),
    # location
    path("check-state/", views.check_state, name="check-state"),
    path("check-district/", views.check_district, name="check-district"),
    path("check-city/", views.check_city, name="check-city"),
    # Wishlist
    path("add_to_wishlist/<int:pk>/", views.add_to_wishlist, name="add_to_wishlist"),
]

urlpatterns += hmtx_views
