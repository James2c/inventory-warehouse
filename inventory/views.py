from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.db.models.deletion import ProtectedError
from django.db import transaction, models

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import ProductForm, WarehouseForm, InventoryForm, StockAdjustmentForm, StockTransferForm, CategoryForm
from .models import Category, Inventory, Product, Supplier, Warehouse, StockAdjustment



def dashboard(request):

    total_products = Product.objects.count()

    total_units = (
        Inventory.objects.aggregate(
            total=Sum("quantity")
        )["total"]
        or 0
    )

    total_warehouses = Warehouse.objects.count()

    low_stock_count = Inventory.objects.filter(
        quantity__lte=models.F("product__reorder_level")
    ).count()

    low_stock_items = (
        Inventory.objects
        .select_related(
            "product",
            "warehouse",
        )
        .filter(
            quantity__lte=models.F("product__reorder_level")
        )
        .order_by(
            "quantity",
        )[:5]
    )

    warehouse_inventory = (
        Warehouse.objects
        .annotate(
            product_count=Count("inventory__product", distinct=True),
            total_units=Sum("inventory__quantity"),
        )
        .order_by("name")
    )

    recent_activity = (
        StockAdjustment.objects
        .select_related(
            "inventory__product",
            "inventory__warehouse",
        )
        .order_by(
            "-created_at",
        )[:10]
    )

    return render(
        request,
        "inventory/dashboard.html",
        {
            "total_products": total_products,
            "total_units": total_units,
            "total_warehouses": total_warehouses,
            "low_stock_count": low_stock_count,
            "warehouse_inventory": warehouse_inventory,
            "low_stock_items": low_stock_items,
            "recent_activity": recent_activity,
        },
    )


def product_list(request):
    products = Product.objects.select_related(
        "category",
        "supplier",
    )

    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    supplier_id = request.GET.get("supplier", "")
    status = request.GET.get("status", "")

    selected_category = (
        int(category_id)
        if category_id.isdigit()
        else None
    )

    selected_supplier = (
        int(supplier_id)
        if supplier_id.isdigit()
        else None
    )

    if query:
        products = products.filter(
            Q(sku__icontains=query)
            | Q(name__icontains=query)
            | Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    if supplier_id:
        products = products.filter(
            supplier_id=supplier_id
        )

    if status == "active":
        products = products.filter(active=True)

    elif status == "inactive":
        products = products.filter(active=False)

    paginator = Paginator(products, 10)

    page_number = request.GET.get("page")

    products = paginator.get_page(page_number)

    return render(
        request,
        "inventory/product_list.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "suppliers": Supplier.objects.all(),
            "query": query,
            "selected_category": selected_category,
            "selected_supplier": selected_supplier,
            "selected_status": status,
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related(
            "category",
            "supplier",
        ),
        id=product_id,
    )

    inventory = Inventory.objects.filter(
        product=product
    ).select_related(
        "warehouse",
    )

    return render(
        request,
        "inventory/product_detail.html",
        {
            "product": product,
            "inventory": inventory,
        },
    )


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()

            return redirect(
                "product_detail",
                product_id=product.id,
            )

    else:
        form = ProductForm()

    return render(
        request,
        "inventory/product_form.html",
        {
            "form": form,
            "page_title": "Add Product",
        },
    )


def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            instance=product,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "product_detail",
                product_id=product.id,
            )

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "inventory/product_form.html",
        {
            "form": form,
            "page_title": "Edit Product",
        },
    )


def product_delete(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
    )

    if request.method == "POST":

        try:
            product.delete()

        except ProtectedError:
            return render(
                request,
                "inventory/product_confirm_delete.html",
                {
                    "product": product,
                    "delete_error": True,
                },
            )

        return redirect("product_list")

    return render(
        request,
        "inventory/product_confirm_delete.html",
        {
            "product": product,
        },
    )


def warehouse_list(request):
    warehouses = Warehouse.objects.all()

    return render(
        request,
        "inventory/warehouse_list.html",
        {
            "warehouses": warehouses,
        },
    )


def warehouse_detail(request, warehouse_id):
    warehouse = get_object_or_404(
        Warehouse,
        id=warehouse_id,
    )

    inventory = warehouse.inventory.select_related(
        "product",
    ).order_by(
        "product__name"
    )

    total_units = inventory.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    low_stock_count = sum(
        1
        for item in inventory
        if item.quantity <= item.product.reorder_level
    )

    return render(
        request,
        "inventory/warehouse_detail.html",
        {
            "warehouse": warehouse,
            "inventory": inventory,
            "product_count": inventory.count(),
            "total_units": total_units,
            "low_stock_count": low_stock_count,
        },
    )


def warehouse_create(request):

    if request.method == "POST":

        form = WarehouseForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("warehouse_list")

    else:

        form = WarehouseForm()

    return render(
        request,
        "inventory/warehouse_form.html",
        {
            "form": form,
            "title": "Add Warehouse",
        },
    )


def warehouse_edit(request, warehouse_id):

    warehouse = get_object_or_404(
        Warehouse,
        id=warehouse_id,
    )

    if request.method == "POST":

        form = WarehouseForm(
            request.POST,
            instance=warehouse,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "warehouse_detail",
                warehouse_id=warehouse.id,
            )

    else:

        form = WarehouseForm(
            instance=warehouse,
        )

    return render(
        request,
        "inventory/warehouse_form.html",
        {
            "form": form,
            "title": "Edit Warehouse",
            "warehouse": warehouse,
        },
    )


def warehouse_delete(request, warehouse_id):

    warehouse = get_object_or_404(
        Warehouse,
        id=warehouse_id,
    )

    if request.method == "POST":

        try:

            warehouse.delete()

        except ProtectedError:

            return render(
                request,
                "inventory/warehouse_confirm_delete.html",
                {
                    "warehouse": warehouse,
                    "protected": True,
                },
            )

        return redirect("warehouse_list")

    return render(
        request,
        "inventory/warehouse_confirm_delete.html",
        {
            "warehouse": warehouse,
            "protected": False,
        },
    )


def inventory_list(request):

    inventory = Inventory.objects.select_related(
        "product",
        "warehouse",
    ).order_by(
        "product__name",
    )

    return render(
        request,
        "inventory/inventory_list.html",
        {
            "inventory": inventory,
        },
    )


def inventory_create(request):

    if request.method == "POST":

        form = InventoryForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("inventory_list")

    else:

        form = InventoryForm()

    return render(
        request,
        "inventory/inventory_form.html",
        {
            "form": form,
            "title": "Add Inventory",
        },
    )


def inventory_edit(request, inventory_id):

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
    )

    if request.method == "POST":

        form = InventoryForm(
            request.POST,
            instance=inventory,
        )

        if form.is_valid():

            form.save()

            return redirect("inventory_list")

    else:

        form = InventoryForm(
            instance=inventory,
        )

    return render(
        request,
        "inventory/inventory_form.html",
        {
            "form": form,
            "title": "Edit Inventory",
            "inventory": inventory,
        },
    )


def inventory_delete(request, inventory_id):

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
    )

    if request.method == "POST":

        inventory.delete()

        return redirect("inventory_list")

    return render(
        request,
        "inventory/inventory_confirm_delete.html",
        {
            "inventory": inventory,
        },
    )


def stock_adjustment_create(request, inventory_id):

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
    )

    if request.method == "POST":

        form = StockAdjustmentForm(request.POST)

        if form.is_valid():

            adjustment = form.save(commit=False)

            adjustment.inventory = inventory

            if (
                adjustment.adjustment_type == "OUT"
                and adjustment.quantity > inventory.quantity
            ):
                form.add_error(
                    "quantity",
                    "Stock out quantity cannot exceed current inventory.",
                )

            else:

                with transaction.atomic():

                    adjustment.save()

                    if adjustment.adjustment_type == "IN":
                        inventory.quantity += adjustment.quantity

                    else:
                        inventory.quantity -= adjustment.quantity

                    inventory.save()

                return redirect("inventory_list")

    else:

        form = StockAdjustmentForm()

    return render(
        request,
        "inventory/stock_adjustment_form.html",
        {
            "form": form,
            "inventory": inventory,
        },
    )


def inventory_history(request, inventory_id):

    inventory = get_object_or_404(
        Inventory,
        id=inventory_id,
    )

    adjustments = inventory.adjustments.order_by(
        "-created_at"
    )

    return render(
        request,
        "inventory/inventory_history.html",
        {
            "inventory": inventory,
            "adjustments": adjustments,
        },
    )


def low_stock(request):

    inventory = Inventory.objects.select_related(
        "product",
        "warehouse",
    ).filter(
        quantity__lte=models.F("product__reorder_level")
    ).order_by(
        "quantity",
    )

    return render(
        request,
        "inventory/low_stock.html",
        {
            "inventory": inventory,
        },
    )


def stock_transfer(request):

    if request.method == "POST":

        form = StockTransferForm(request.POST)

        if form.is_valid():

            product = form.cleaned_data["product"]
            from_warehouse = form.cleaned_data["from_warehouse"]
            to_warehouse = form.cleaned_data["to_warehouse"]
            quantity = form.cleaned_data["quantity"]
            reason = form.cleaned_data["reason"]

            source_inventory = form.cleaned_data[
                "source_inventory"
            ]

            if quantity > source_inventory.quantity:

                form.add_error(
                    "quantity",
                    "Transfer quantity cannot exceed "
                    "available source inventory.",
                )

            else:

                with transaction.atomic():

                    destination_inventory, created = (
                        Inventory.objects.get_or_create(
                            product=product,
                            warehouse=to_warehouse,
                            defaults={
                                "quantity": 0,
                            },
                        )
                    )

                    source_inventory.quantity -= quantity

                    destination_inventory.quantity += quantity

                    source_inventory.save()

                    destination_inventory.save()

                    StockAdjustment.objects.create(
                        inventory=source_inventory,
                        adjustment_type="OUT",
                        quantity=quantity,
                        reason=(
                            reason
                            or f"Transfer to {to_warehouse.name}"
                        ),
                    )

                    StockAdjustment.objects.create(
                        inventory=destination_inventory,
                        adjustment_type="IN",
                        quantity=quantity,
                        reason=(
                            reason
                            or f"Transfer from {from_warehouse.name}"
                        ),
                    )

                return redirect("inventory_list")

    else:

        form = StockTransferForm()

    return render(
        request,
        "inventory/stock_transfer_form.html",
        {
            "form": form,
        },
    )


def stock_activity(request):

    activities = (
        StockAdjustment.objects
        .select_related(
            "inventory__product",
            "inventory__warehouse",
        )
        .order_by("-created_at")
    )

    products = Product.objects.order_by("name")

    warehouses = Warehouse.objects.order_by("name")

    selected_product = request.GET.get("product", "")
    selected_warehouse = request.GET.get("warehouse", "")
    selected_type = request.GET.get("type", "")

    if selected_product:
        activities = activities.filter(
            inventory__product_id=selected_product
        )

    if selected_warehouse:
        activities = activities.filter(
            inventory__warehouse_id=selected_warehouse
        )

    if selected_type:
        activities = activities.filter(
            adjustment_type=selected_type
        )

    paginator = Paginator(activities, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "inventory/stock_activity.html",
        {
            "activities": page_obj,
            "page_obj": page_obj,
            "products": products,
            "warehouses": warehouses,
            "selected_product": selected_product,
            "selected_warehouse": selected_warehouse,
            "selected_type": selected_type,
        },
    )



def category_list(request):

    categories = (
        Category.objects
        .annotate(
            product_count=Count("products")
        )
        .order_by("name")
    )

    return render(
        request,
        "inventory/category_list.html",
        {
            "categories": categories,
        },
    )


def category_create(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            category = form.save()

            return redirect(
                "category_detail",
                category_id=category.id,
            )

    else:

        form = CategoryForm()

    return render(
        request,
        "inventory/category_form.html",
        {
            "form": form,
            "title": "Add Category",
            "submit_label": "Create Category",
        },
    )


def category_detail(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    products = (
        Product.objects
        .filter(category=category)
        .order_by("name")
    )

    return render(
        request,
        "inventory/category_detail.html",
        {
            "category": category,
            "products": products,
        },
    )


def category_edit(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            instance=category,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "category_detail",
                category_id=category.id,
            )

    else:

        form = CategoryForm(
            instance=category,
        )

    return render(
        request,
        "inventory/category_form.html",
        {
            "form": form,
            "title": "Edit Category",
            "submit_label": "Save Changes",
        },
    )


def category_delete(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    if request.method == "POST":

        try:

            category.delete()

        except ProtectedError:

            return render(
                request,
                "inventory/category_delete.html",
                {
                    "category": category,
                    "error": (
                        "This category cannot be deleted "
                        "because products are assigned to it."
                    ),
                },
            )

        return redirect("category_list")

    return render(
        request,
        "inventory/category_delete.html",
        {
            "category": category,
        },
    )