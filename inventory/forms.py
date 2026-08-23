from django import forms

from .models import Product, Warehouse, Inventory


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