from django.urls import path
from .api import search_dishes
from .views import SearchPage
from .views import DishListView, DishCreateView, DishUpdateView, DishDeleteView, ReviewCreateView, DishDetailView
app_name = 'restaurants'   # ← добавляем namespace, очень полезно

urlpatterns = [
    path('', SearchPage.as_view(), name='search_page'),
    path('search/', search_dishes, name='search_api'),
     path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishes/add/', DishCreateView.as_view(), name='dish-add'),
    path('dishes/<int:pk>/edit/', DishUpdateView.as_view(), name='dish-edit'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),
    path('dishes/<int:dish_id>/review/', ReviewCreateView.as_view(), name='add-review'),
    # restaurants/urls.py — добавь эту строку
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
]
