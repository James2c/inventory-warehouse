from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.db.models.deletion import ProtectedError

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import ProductForm, WarehouseForm, InventoryForm
from .models import Category, Inventory, Product, Supplier, Warehouse



def dashboard(request):
    return render(request, "inventory/dashboard.html")


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