from django.views.generic import TemplateView

class SearchPage(TemplateView):
    template_name = "restaurants/search.html"
