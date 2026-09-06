from django import forms

from .models import (
    Product, 
    Warehouse, 
    Inventory, 
    StockAdjustment, 
    Category, 
    Supplier, 
    PurchaseOrder, 
    PurchaseOrderItem, 
    PurchaseOrderAttachment,
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "sku",
            "name",
            "description",
            "category",
            "supplier",
            "unit_price",
            "reorder_level",
            "active",
        ]

        widgets = {
            "sku": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "supplier": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

            "reorder_level": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class WarehouseForm(forms.ModelForm):

    class Meta:
        model = Warehouse
        fields = [
            "name",
            "location",
            "active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Warehouse name",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City, Province",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory

        fields = [
            "product",
            "warehouse",
            "quantity",
        ]

        widgets = {
            "product": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "warehouse": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }


class StockAdjustmentForm(forms.ModelForm):

    class Meta:
        model = StockAdjustment
        fields = [
            "adjustment_type",
            "quantity",
            "reason",
        ]

        widgets = {
            "adjustment_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
            "reason": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Reason for adjustment",
                }
            ),
        }


class StockTransferForm(forms.Form):

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    from_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    to_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 1,
            }
        ),
    )

    reason = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Reason for transfer",
            }
        ),
    )

    def clean(self):

        cleaned_data = super().clean()

        product = cleaned_data.get("product")
        from_warehouse = cleaned_data.get("from_warehouse")
        to_warehouse = cleaned_data.get("to_warehouse")

        if (
            from_warehouse
            and to_warehouse
            and from_warehouse == to_warehouse
        ):
            raise forms.ValidationError(
                "Source and destination warehouses must be different."
            )

        if product and from_warehouse:

            inventory = Inventory.objects.filter(
                product=product,
                warehouse=from_warehouse,
            ).first()

            if not inventory:
                raise forms.ValidationError(
                    "No inventory exists for this product "
                    "at the source warehouse."
                )

            cleaned_data["source_inventory"] = inventory

        return cleaned_data


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [
            "name",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class SupplierForm(forms.ModelForm):

    class Meta:

        model = Supplier

        fields = [
            "name",
            "contact_name",
            "email",
            "phone",
            "address",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "contact_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class PurchaseOrderForm(forms.ModelForm):

    class Meta:

        model = PurchaseOrder

        fields = [
            "supplier",
            "warehouse",
            "order_date",
            "expected_date",
            "shipping_cost",
            "notes",
        ]

        widgets = {

            "supplier": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "warehouse": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "order_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "expected_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "shipping_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class PurchaseOrderItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderItem

        fields = [
            "product",
            "quantity_ordered",
        ]

        widgets = {
            "product": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "quantity_ordered": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
        }

    def __init__(
        self,
        *args,
        purchase_order=None,
        **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.purchase_order = purchase_order

    def clean_product(self):

        product = self.cleaned_data["product"]

        queryset = PurchaseOrderItem.objects.filter(
            purchase_order=self.purchase_order,
            product=product,
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise forms.ValidationError(
                "This product has already been added "
                "to this purchase order."
            )

        return product


class PurchaseOrderReceiveForm(forms.Form):

    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 1,
            }
        ),
    )


class PurchaseOrderAttachmentForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderAttachment

        fields = [
            "file",
            "description",
        ]

        widgets = {
            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Supplier Quote",
                }
            ),
        }