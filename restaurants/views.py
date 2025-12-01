# restaurants/views.py — правильные импорты
from winreg import DeleteKey
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ingredient, Restaurant, RestaurantDish, Review, Dish
from .forms import DishForm, RestaurantDishForm, ReviewForm
from restaurants import models   # ← теперь будет работать


class SearchPage(TemplateView): # type: ignore
    template_name = "restaurants/search.html"


class OwnerRequiredMixin(UserPassesTestMixin): # type: ignore
    def test_func(self):
        return self.request.user.groups.filter(name='Owner').exists()


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'restaurants/dishes_list.html'


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'restaurants/dishes_form.html'
    success_url = reverse_lazy('restaurants:dish-list')    # ← дефис!

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff


class DishUpdateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'restaurants/dishes_form.html'
    success_url = reverse_lazy('restaurants:dish-list')    # ← дефис!

    def test_func(self):
        return self.request.user.is_staff
    
class DishDeleteView(LoginRequiredMixin, DeleteKey):
    model = Dish
    template_name = 'restaurants/dishes_confirm_delete.html'
    success_url = reverse_lazy('restaurants:dish-list')    # ← дефис!

    def test_func(self):
        return self.request.user.is_staff
    
# ← ВНИМАНИЕ: ЭТОТ КЛАСС ДОЛЖЕН БЫТЬ НА ТОМ ЖЕ УРОВНЕ, НЕ ВНУТРИ ДРУГОГО!
class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    template_name = 'restaurants/dish_detail.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['review_form'] = ReviewForm()
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'restaurants/reviews_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # обязательно author, не user
        form.instance.dish_id = self.kwargs['dish_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('restaurants:dish-detail', kwargs={'pk': self.kwargs['dish_id']})


class Dish(models.Model):
    name = models.CharField(max_length=200)
    base_description = models.TextField(blank=True)

    def __str__(self):
        return self.name

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

    # уникально для каждого ресторана
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dish.name} — {self.restaurant.name}"


class Review(models.Model):
    item = models.ForeignKey(
        RestaurantDish,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE) # type: ignore

    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} — {self.item} — {self.rating}★"

class RestaurantDishCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantDishForm
    template_name = 'restaurants/dish_form.html'

    def form_valid(self, form):
        restaurant = Restaurant.objects.get(owner=self.request.user)
        form.save(restaurant=restaurant)
        return redirect('restaurant-menu')
