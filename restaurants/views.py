from django.views.generic import TemplateView

class SearchPage(TemplateView):
    template_name = "restaurants/search.html"

from .models import Review
from .forms import ReviewForm

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Dish
from .forms import DishForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Owner').exists()

class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'dishes/list.html'

class DishCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'dishes/form.html'
    success_url = reverse_lazy('dish-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class DishUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'dishes/form.html'
    success_url = reverse_lazy('dish-list')

class DishDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Dish
    template_name = 'dishes/confirm_delete.html'
    success_url = reverse_lazy('dish-list')


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.dish_id = self.kwargs['dish_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dish-detail', kwargs={'pk': self.kwargs['dish_id']})