from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="products"
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reorder_level = models.PositiveIntegerField(default=0)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    manager = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PurchaseOrderNumberSequence(models.Model):
    next_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Next PO Number: {self.next_number}"
     

class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("ordered", "Ordered"),
        ("partially_received", "Partially Received"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    ]

    po_number = models.CharField(
        max_length=50,
        unique=True,
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
    )

    order_date = models.DateField()

    expected_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="draft",
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.po_number

    def can_edit(self):
        return self.status == "draft"


    def can_receive(self):
        return self.status in ["ordered", "partially_received"]


    def is_complete(self):
        return self.status == "received"


class PurchaseOrderItem(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_order_items",
    )

    quantity_ordered = models.PositiveIntegerField()

    quantity_received = models.PositiveIntegerField(
        default=0,
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def quantity_remaining(self):
        return self.quantity_ordered - self.quantity_received

    def line_total(self):
        return self.quantity_ordered * self.unit_price

    def receive(self, quantity):
        self.quantity_received += quantity
        self.save(update_fields=["quantity_received"])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["purchase_order", "product"],
                name="unique_purchase_order_product",
            )
        ]

    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.name}"
    

class Inventory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="inventory",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="inventory"
    )

    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "warehouse"],
                name="unique_product_warehouse"
            )
        ]

    def __str__(self):
        return f"{self.product} - {self.warehouse}"


class StockAdjustment(models.Model):

    ADJUSTMENT_TYPES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="adjustments",
    )

    adjustment_type = models.CharField(
        max_length=3,
        choices=ADJUSTMENT_TYPES,
    )

    quantity = models.PositiveIntegerField()

    reason = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.inventory.product.name} - "
            f"{self.get_adjustment_type_display()} - "
            f"{self.quantity}"
        )


class InventoryTransaction(models.Model):

    TRANSACTION_TYPES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
        ("ADJUSTMENT", "Adjustment"),
        ("TRANSFER", "Transfer"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.IntegerField()

    reference = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.product} - "
            f"{self.transaction_type} - "
            f"{self.quantity}"
        )