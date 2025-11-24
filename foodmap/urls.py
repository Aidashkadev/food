"""
URL configuration for foodmap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# foodmap/foodmap/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ВСЁ ТВОЁ ПРИЛОЖЕНИЕ СРАЗУ НА КОРЕНЬ — это то, что ты хочешь!
    path('', include('restaurants.urls')),
    
    # Если хочешь, чтобы старый адрес /restaurants/ тоже работал — оставь эту строку,
    # она не мешает:
    path('restaurants/', include('restaurants.urls')),
]


