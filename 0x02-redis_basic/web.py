#!/usr/bin/env python3
"""
Module for caching and counting web page requests using Redis.

This module defines a decorator to count the number of times a URL is requested
and to cache the HTML content of the URL for a specified period of time.
"""

import redis
import requests
from functools import wraps


def count_requests(expiration: int):
    """
    Decorator to count number of times a URL is requested and cache the result.
    """

    def decorator(method):
        """
        Wrapper function to count requests and cache the HTML content.
        """

        @wraps(method)
        def wrapper(url: str):
            """
            Wrapper function to count requests and cache the HTML content.
            """

            redis_client = redis.Redis()
            cache_key = f"page:{url}"
            count_key = f"count:{url}"
            redis_client.incr(count_key)
            cached_html = redis_client.get(cache_key)
            if cached_html:
                return cached_html
            result = method(url)
            redis_client.setex(cache_key, expiration, result)
            return result

        return wrapper
    return decorator


@count_requests(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """

    response = requests.get(url)
    return response.text
