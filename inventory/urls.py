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

    path(
        "warehouses/",
        views.warehouse_list,
        name="warehouse_list",
    ),

    path(
        "warehouses/add/",
        views.warehouse_create,
        name="warehouse_create",
    ),

    path(
        "warehouses/<int:warehouse_id>/edit/",
        views.warehouse_edit,
        name="warehouse_edit",
    ),

    path(
        "warehouses/<int:warehouse_id>/delete/",
        views.warehouse_delete,
        name="warehouse_delete",
    ),

    path(
        "warehouses/<int:warehouse_id>/",
        views.warehouse_detail,
        name="warehouse_detail",
    ),
]