from django.core.management.base import BaseCommand
from hw_app.models import Product
from datetime import date


class Command(BaseCommand):
    help = "Create product"

    def handle(self, *args, **kwargs):
        product = Product(name='Джинсы', description='красивые, синего цвета, размер 29', price=2000, quantity=2,
                          data_addition=date.today)

        product.save()
        self.stdout.write(f'{product}')