
from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    """Create Order"""

    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write("no order found")
            return
        products = Product.objects.all()

        for product in products:
            order.products.add(product)

        order.save()
        self.stdout.write(f"order update {order.products.all()} to order {order}")
