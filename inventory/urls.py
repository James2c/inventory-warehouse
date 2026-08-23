from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path(
        "products/", 
        views.product_list, 
        name="product_list"),

    path(
        "products/<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),

    path(
        "products/add/",
        views.product_create,
        name="product_create",
    ),

    path(
        "products/<int:product_id>/edit/",
        views.product_edit,
        name="product_edit",
    ),

    path(
        "products/<int:product_id>/delete/",
        views.product_delete,
        name="product_delete",
    ),
]