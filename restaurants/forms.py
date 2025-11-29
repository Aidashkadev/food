from django import forms
from .models import RestaurantDish, Dish

class DishCreateForm(forms.ModelForm):
    dish_name = forms.CharField(max_length=200, label="Название блюда")

    class Meta:
        model = RestaurantDish
        fields = ['dish_name', 'description', 'price', 'ingredients']

    def save(self, commit=True, restaurant=None):
        # создаём или получаем Dish
        dish_name = self.cleaned_data['dish_name']
        dish, created = Dish.objects.get_or_create(name=dish_name)

        # создаём RestaurantDish
        restaurant_dish = super().save(commit=False)
        restaurant_dish.dish = dish
        if restaurant:
            restaurant_dish.restaurant = restaurant

        if commit:
            restaurant_dish.save()
            self.save_m2m()

        return restaurant_dish
