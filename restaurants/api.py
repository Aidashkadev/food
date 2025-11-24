# restaurants/api.py
from django.http import JsonResponse
from .models import Dish
from django.db.models import Q

def search_dishes(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse([], safe=False)
    
    # Ищем по названию блюда ИЛИ по названию ресторана, без учёта регистра
    dishes = Dish.objects.filter(
        Q(name__icontains=query) | Q(restaurant__name__icontains=query)
    ).select_related('restaurant').values(
        'id', 'name', 'price', 'restaurant__name'
    )
    
    # Приводим к удобному виду
    result = [
        {
            'id': dish['id'],
            'name': dish['name'],
            'price': dish['price'],
            'restaurant': dish['restaurant__name']
        }
        for dish in dishes
    ]
    
    return JsonResponse(result, safe=False)