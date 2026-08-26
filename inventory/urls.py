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
        "inventory/",
        views.inventory_list,
        name="inventory_list",
    ),

    path(
        "inventory/low-stock/",
        views.low_stock,
        name="low_stock",
    ),

    path(
        "inventory/add/",
        views.inventory_create,
        name="inventory_create",
    ),

    path(
        "warehouses/add/",
        views.warehouse_create,
        name="warehouse_create",
    ),

    path(
        "inventory/<int:inventory_id>/edit/",
        views.inventory_edit,
        name="inventory_edit",
    ),

    path(
        "inventory/<int:inventory_id>/delete/",
        views.inventory_delete,
        name="inventory_delete",
    ),

    path(
        "inventory/<int:inventory_id>/adjust/",
        views.stock_adjustment_create,
        name="stock_adjustment_create",
    ),

    path(
        "inventory/<int:inventory_id>/history/",
        views.inventory_history,
        name="inventory_history",
    ),

    path(
        "inventory/transfer/",
        views.stock_transfer,
        name="stock_transfer",
    ),

    path(
        "adjustments/",
        views.stock_activity,
        name="stock_activity",
    ),

    path(
        "categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "categories/create/",
        views.category_create,
        name="category_create",
    ),

    path(
        "categories/<int:category_id>/",
        views.category_detail,
        name="category_detail",
    ),

    path(
        "categories/<int:category_id>/edit/",
        views.category_edit,
        name="category_edit",
    ),

    path(
        "categories/<int:category_id>/delete/",
        views.category_delete,
        name="category_delete",
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