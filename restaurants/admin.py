from django.contrib import admin
from .models import Restaurant, Dish, Category, Ingredient   # ← Review убрали


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude', 'is_open')


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_filter = ('restaurant', 'category')


admin.site.register(Category)
admin.site.register(Ingredient)