from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.deletion import ProtectedError

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import ProductForm
from .models import Category, Inventory, Product, Supplier



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