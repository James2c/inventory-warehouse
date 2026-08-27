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
        "stock-transfers/history/",
        views.stock_transfer_history,
        name="stock_transfer_history",
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
        "suppliers/",
        views.supplier_list,
        name="supplier_list",
    ),

    path(
        "suppliers/create/",
        views.supplier_create,
        name="supplier_create",
    ),

    path(
        "suppliers/<int:supplier_id>/delete/",
        views.supplier_delete,
        name="supplier_delete",
    ),

    path(
        "suppliers/<int:supplier_id>/edit/",
        views.supplier_edit,
        name="supplier_edit",
    ),

    path(
        "suppliers/<int:supplier_id>/",
        views.supplier_detail,
        name="supplier_detail",
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

    path(
        "purchase-orders/",
        views.purchase_order_list,
        name="purchase_order_list",
    ),

    path(
        "purchase-orders/create/",
        views.purchase_order_create,
        name="purchase_order_create",
    ),

    path(
        "purchase-orders/<int:purchase_order_id>/items/add/",
        views.purchase_order_item_create,
        name="purchase_order_item_create",
    ),

    path(
        "purchase-orders/<int:purchase_order_id>/items/<int:item_id>/edit/",
        views.purchase_order_item_edit,
        name="purchase_order_item_edit",
    ),

    path(
        "purchase-orders/<int:purchase_order_id>/items/<int:item_id>/delete/",
        views.purchase_order_item_delete,
        name="purchase_order_item_delete",
    ),

    path(
        "purchase-orders/<int:purchase_order_id>/items/<int:item_id>/receive/",
        views.purchase_order_item_receive,
        name="purchase_order_item_receive",
    ),

    path(
        "purchase-orders/<int:purchase_order_id>/",
        views.purchase_order_detail,
        name="purchase_order_detail",
    ),
]