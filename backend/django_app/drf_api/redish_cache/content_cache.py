import redis

# Connect to Redis
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)

def store_movie_click(movie_id):
    redis_client.sadd("clicked_movies", movie_id)

def get_clicked_movies():
    """ Retrieve all clicked movie IDs from Redis """
    return list(redis_client.smembers("clicked_movies"))


from django.core.cache import caches

# Use default cache (Redis DB 1)
default_cache = caches["default"]
default_cache.set("user:1", "Jewish", timeout=600)  # Store for 10 minutes
print(default_cache.get("user:1"))  # Output: Jewish

# Use secondary cache (Redis DB 2)
secondary_cache = caches["secondary"]
secondary_cache.set("user:2", "Alice", timeout=600)
print(secondary_cache.get("user:2"))  # Output: Alice
