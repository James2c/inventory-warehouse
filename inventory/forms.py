from django import forms

from .models import Product, Warehouse, Inventory, StockAdjustment, Category


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