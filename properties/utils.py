import logging
from django_redis import get_redis_connection
from django.core.cache import cache
from .models import Property


logger = logging.getlogger(__nme__)

def get_all_properties():
    # Try To get from cache
    properties = cache.get('all_properties')

    if not properties:
        # Cache miss, fetch from database
        properties = list(Property.objects.all().values())
        # Store in cache for future requests
        cache.set('all_properties', properties, timeout=3600)  # Cache for 1 hour

    return properties

def get_redis_cache_metrics():
    """
    Retrive Redis cache metrics: hits, misses and hit ratio
    """
    conn = get_redis_connection("default")
    info = conn.info("stats") # get Redis stats

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2)
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics