from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import ProductForm
from .models import Inventory, Product


def dashboard(request):
    return render(request, "inventory/dashboard.html")


def product_list(request):
    products = Product.objects.select_related(
        "category",
        "supplier",
    )

    return render(
        request,
        "inventory/product_list.html",
        {"products": products},
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