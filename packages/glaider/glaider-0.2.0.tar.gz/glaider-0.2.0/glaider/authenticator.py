from functools import wraps
import os
import requests


def check_api_key(func):
    """Wrapper that checks if an api key is correctly instantiated"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the 'self' instance from args if present
        instance = args[0] if args else None

        glaider_api_key = getattr(instance, '_glaider_api_key', None) or os.getenv('GLAIDER_API_KEY')

        if not glaider_api_key:
            raise ValueError("missing glaider API key, make sure glaider is initialized correctly")

        return func(*args, **kwargs)
    return wrapper


def is_valid(api_key: str):
    """Checks if the API is authenticated"""
    return requests.post('https://api.glaider.it/check-cid',
                         json={'cid': api_key},
                         headers={'Content-Type': 'application/json'}).status_code == 200