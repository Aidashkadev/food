from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Dish, Review
from .forms import DishForm, ReviewForm


class SearchPage(TemplateView):
    template_name = "restaurants/search.html"


class OwnerRequiredMixin(UserPassesTestMixin):
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


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'restaurants/dishes_form.html'
    success_url = reverse_lazy('restaurants:dish-list')    # ← дефис!

    def test_func(self):
        return self.request.user.is_staff
    
class DishDeleteView(LoginRequiredMixin, DeleteView):
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

 


