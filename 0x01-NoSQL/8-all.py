#!/usr/bin/env python3

"""
A function to list all documents in a MongoDB collection.
"""


def list_all(mongo_collection):
    """
    Returns a list of all documents in the specified MongoDB collection.

    Args:
        mongo_collection: pymongo collection object
        representing the MongoDB collection.

    Returns:
        A list containing all documents in the collection.
    """
    return list(mongo_collection.find())
