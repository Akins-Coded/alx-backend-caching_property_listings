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
    Retrieve Redis cache metrics: hits, misses, and hit ratio.
    Logs errors if Redis is unavailable.
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info("stats")  # fetch Redis stats

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        if total_requests > 0:
            hit_ratio = hits / total_requests
        else:
            hit_ratio = 0.0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0.0,
        }