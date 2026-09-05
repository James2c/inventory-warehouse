from django.core.management.base import BaseCommand

from inventory.models import PurchaseOrderItem


class Command(BaseCommand):
    help = "Backfill zero-priced PO items using the current Product unit price."

    def handle(self, *args, **options):

        items = (
            PurchaseOrderItem.objects
            .filter(unit_price=0)
            .select_related("product", "purchase_order")
        )

        updated_count = 0

        for item in items:

            item.unit_price = item.product.unit_price

            item.save(update_fields=["unit_price"])

            updated_count += 1

            self.stdout.write(
                f"{item.purchase_order.po_number} - "
                f"{item.product.name}: "
                f"${item.unit_price:.2f}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated {updated_count} PO item(s)."
            )
        )