from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try To get from cache
    properties = cache.get('all_properties')

    if not properties:
        # Cache miss, fetch from database
        properties = list(Property.objects.all().values())
        # Store in cache for future requests
        cache.set('all_properties', properties, timeout=3600)  # Cache for 1 hour

    return properties
