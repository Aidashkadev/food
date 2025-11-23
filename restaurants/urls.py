from django.urls import path
# from .api import search_dishes
from .views import SearchPage

urlpatterns = [
    path('', SearchPage.as_view(), name='search_page'),
    # path('search/', search_dishes, name='search_api'),
]
