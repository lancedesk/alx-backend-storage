#!/usr/bin/env python3
"""
Module for caching and counting web page requests using Redis.

This module defines a decorator to count the number of times a URL is requested
and to cache the HTML content of the URL for a specified period of time.
"""

import redis
import requests
from typing import Callable
from functools import wraps


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count number of times a URL is requested and cache the result.
    """

    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function to count requests and cache the HTML content.
        """

        redis_client = redis.Redis()
        redis_client.incr(f'count:{url}')
        cached_html = redis_client.get(f'{url}')
        if cached_html:
            return cached_html.decode('utf-8')
        response = method(url)
        redis_client.set(f'{url}', response, 10)
        return response
    return wrapper


@count_requests
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
