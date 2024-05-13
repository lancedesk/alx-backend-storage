#!/usr/bin/env python3
"""
A function to insert a new document into a MongoDB collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the specified MongoDB collection
    based on provided keyword arguments.

    Args:
        mongo_collection: pymongo collection object representing
        the MongoDB collection.
        **kwargs: Keyword arguments representing the fields
        and values of the new document.

    Returns:
        The _id of the newly inserted document.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
