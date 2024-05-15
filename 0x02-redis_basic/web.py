#!/usr/bin/env python3
"""
Module for caching and counting web page requests using Redis.

This module defines a decorator to count the number of times a URL is requested
and to cache the HTML content of the URL for a specified period of time.
"""

import requests
import time
from functools import wraps
from typing import Dict

"""
Separate dictionaries for storing cached web page contents
and cached counts with timestamps
"""

page_cache: Dict[str, str] = {}
request_cache: Dict[str, tuple] = {}

def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL from cache or fetches it from the web.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """

    if url in page_cache:
        print(f"Retrieving from cache: {url}")
        return page_cache[url]
    else:
        print(f"Retrieving from web: {url}")
        response = requests.get(url)
        result = response.text
        page_cache[url] = result
        return result

def cache_with_expiration(expiration: int):
    """
    Decorator to cache the HTML content of a URL with expiration time.

    Args:
        expiration (int): The expiration time for cached content in seconds.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            count_key = f"count:{url}"
            if count_key in request_cache:
                count, timestamp = request_cache[count_key]
                if time.time() - timestamp > expiration:
                    result = func(*args, **kwargs)
                    request_cache[count_key] = (count + 1, time.time())
                    return result
                else:
                    request_cache[count_key] = (count + 1, timestamp)
                    return
    return wrapper
    return decorator
