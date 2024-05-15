#!/usr/bin/env python3
"""
Redis tasks...
Implementation of Cache class to handle basic caching operations
using Redis as the backend storage. Supports storing and retrieving
data with custom conversion functions.
"""

import uuid
from functools import wraps
from typing import Callable, Optional, Union

import redis


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a given method.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store method call history.
        """

        meth_name = method.__qualname__
        self._redis.rpush(meth_name + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(meth_name + ":outputs", output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Function to display the history of calls of a given method.
    """

    meth_name = method.__qualname__
    redis_db = method.__self__._redis
    inputs = redis_db.lrange(meth_name + ":inputs", 0, -1)
    outputs = redis_db.lrange(meth_name + ":outputs", 0, -1)

    print(f"{meth_name} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        input = input.decode("utf-8")
        output = output.decode("utf-8")
        print(f"{meth_name}(*{input}) -> {output}")


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count method calls.
        """

        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    def __init__(self) -> None:
        """
        Initialize the Cache instance,
        create a Redis client and flush the database.
        """

        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None,
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the data stored in Redis using the provided key and
        apply the conversion function if provided.
        """

        value = self._redis.get(key)
        if value is not None and fn is not None:
            value = fn(value)
        return value

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve the data stored in Redis using the provided key
        and convert it to an integer.
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve the data stored in Redis using the provided key
        and convert it to a string using UTF-8 decoding.
        """

        return self.get(key, str)
