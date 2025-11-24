from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, Dish

class Command(BaseCommand):
    help = "Loads sample restaurants and dishes"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Deleting old data..."))
        Dish.objects.all().delete()
        Restaurant.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Loading restaurants..."))

        r1 = Restaurant.objects.create(
            name="Ассорти",
            address="Центр Токмока",
            latitude=42.8410,
            longitude=75.3010,
        )

        r2 = Restaurant.objects.create(
            name="Уйгур Лагман",
            address="ул. Ибраимова 15",
            latitude=42.8405,
            longitude=75.3052,
        )

        r3 = Restaurant.objects.create(
            name="Шорпо House",
            address="ул. Садовая 77",
            latitude=42.8388,
            longitude=75.2981,
        )

        self.stdout.write(self.style.SUCCESS("Loading dishes..."))

        Dish.objects.create(name="Лагман", restaurant=r1)
        Dish.objects.create(name="Манты", restaurant=r1)
        Dish.objects.create(name="Бешбармак", restaurant=r1)

        Dish.objects.create(name="Лагман", restaurant=r2)
        Dish.objects.create(name="Гююрма", restaurant=r2)

        Dish.objects.create(name="Шорпо", restaurant=r3)
        Dish.objects.create(name="Плов", restaurant=r3)

        self.stdout.write(self.style.SUCCESS("Done! Sample data loaded."))
