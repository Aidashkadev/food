from django import forms
from .models import Dish, Review

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'restaurant']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

from django.contrib.auth.forms import UserCreationForm
