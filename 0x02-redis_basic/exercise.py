#!/usr/bin/env python3
"""
Redis tasks...
Implementation of Cache class to handle basic caching operations
using Redis as the backend storage. Supports storing and retrieving
data with custom conversion functions.
"""

import uuid
import redis
from functools import wraps
from typing import Callable, Optional, Union


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a given method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with input/output history tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store method call history.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The output of the wrapped method.
        """
        method_name = method.__qualname__
        self._redis.rpush(method_name + ":inputs", str(args))
        output_data = method(self, *args, **kwargs)
        self._redis.rpush(method_name + ":outputs", str(output_data))
        return output_data

    return wrapper


def replay(method: Callable) -> None:
    """
    Function to display the history of calls of a given method.

    Args:
        method (Callable):
        The method for which the call history will be displayed.
    """
    method_name = method.__qualname__
    redis_client = method.__self__._redis
    inputs = redis_client.lrange(method_name + ":inputs", 0, -1)
    outputs = redis_client.lrange(method_name + ":outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        input_data = input_data.decode("utf-8")
        output_data = output_data.decode("utf-8")
        print(f"{method_name}(*{input_data}) -> {output_data}")


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call count tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count method calls.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The output of the wrapped method.
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

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated random key used to store the data.
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

        Args:
            key (str): The key to retrieve the data.
            fn (Optional[Callable]):
            The function to apply to the data for conversion.

        Returns:
            Union[str, bytes, int, float, None]:
            The retrieved data or None if key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve the data stored in Redis using the provided key
        and convert it to an integer.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Union[int, None]:
            The retrieved data as an integer or None if key does not exist.
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve the data stored in Redis using the provided key
        and convert it to a string using UTF-8 decoding.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Union[str, None]:
            The retrieved data as a string or None if key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))
