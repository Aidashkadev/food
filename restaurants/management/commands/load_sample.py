from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, Dish

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        r = Restaurant.objects.create(
            name="Ассорти",
            address="Центр Токмока",
            latitude=42.841,
            longitude=75.301
        )
        Dish.objects.create(name="Лагман", price=200, restaurant=r)
        self.stdout.write(self.style.SUCCESS("Sample data added"))
