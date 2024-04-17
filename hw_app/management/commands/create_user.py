from django.core.management.base import BaseCommand
from hw_app.models import User
from datetime import date


class Command(BaseCommand):
    help = "Create user."

    def handle(self, *args, **kwargs):
        #user = User(name='Andrey', email='andr@example.com', telephone= '8999000000', address='Address', data_registered=date.today)
        user = User(name='Vasay', email='vasay@example.com', telephone= '8999000001', address='Address2', data_registered=date.today)


        user.save()
        self.stdout.write(f'{user}')