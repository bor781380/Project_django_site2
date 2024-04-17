from django.core.management.base import BaseCommand
from hw_app.models import Product


class Command(BaseCommand):
    help = "Get all products."

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        self.stdout.write(f'{products}')