from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property  # adjust if your model is named differently

# Cache for 15 minutes (60 * 15 seconds)
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values("id", "title", "price", "location")  
    return JsonResponse(list(properties), safe=False)
