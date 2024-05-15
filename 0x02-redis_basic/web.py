#!/usr/bin/env python3
"""
Module for caching and counting web page requests using Redis.

This module defines a decorator to count the number of times a URL is requested
and to cache the HTML content of the URL for a specified period of time.
"""

import redis
import requests
from functools import wraps
from typing import Callable
from datetime import timedelta


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count number of times a URL is requested and cache the result.
    """
    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """
        Wrapper function to count requests and cache the HTML content.
        """

        count_key = "count:{}".format(url)
        redis_client = redis.Redis()
        redis_client.incr(count_key)
        result = method(url, *args, **kwargs)
        redis_client.setex(url, timedelta(seconds=10), str(result))

        return result
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
    return requests.get(url).text
