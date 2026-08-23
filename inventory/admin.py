from django.contrib import admin

from .models import (
    Category,
    Supplier,
    Product,
    Warehouse,
    Inventory,
    InventoryTransaction,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact_name",
        "email",
        "phone",
    )
    search_fields = (
        "name",
        "contact_name",
        "email",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "supplier",
        "unit_price",
        "reorder_level",
        "active",
    )

    list_filter = (
        "category",
        "supplier",
        "active",
    )

    search_fields = (
        "sku",
        "name",
        "description",
    )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "manager",
        "active",
    )

    list_filter = ("active",)

    search_fields = (
        "name",
        "location",
        "manager",
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "warehouse",
        "quantity",
    )

    list_filter = (
        "warehouse",
    )

    search_fields = (
        "product__sku",
        "product__name",
        "warehouse__name",
    )


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "warehouse",
        "transaction_type",
        "quantity",
        "reference",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "warehouse",
        "created_at",
    )

    search_fields = (
        "product__sku",
        "product__name",
        "reference",
        "notes",
    )

    readonly_fields = ("created_at",)