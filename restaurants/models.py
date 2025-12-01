


from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse  # <-- добавили это



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=50, blank=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.pk})


# Общее блюдо (например, "Паста Карбонара", "Бургер")
class Dish(models.Model):
    name = models.CharField(max_length=200)
    base_description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dish_detail", kwargs={"pk": self.pk})


# Связь блюда с конкретным рестораном (с ценой, своими ингредиентами и описанием)
class RestaurantDish(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu"
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="restaurant_items"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('restaurant', 'dish')  # одно и то же блюдо не дублируется в меню

    def __str__(self):
        return f"{self.dish.name} — {self.restaurant.name} ({self.price} ₽)"

    def get_absolute_url(self):
        return reverse("restaurantdish_detail", kwargs={"pk": self.pk})


class Review(models.Model):

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews')

    item = models.ForeignKey(
        RestaurantDish,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.author} — {self.rating}★"
    


        return f"{self.author} — {self.rating}★ — {self.item}"
