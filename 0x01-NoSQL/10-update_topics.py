#!/usr/bin/env python3
"""
A function to update the topics of a school document based on the name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document based on the provided name.

    Args:
        mongo_collection: pymongo collection object
        representing the MongoDB collection.
        name: String representing the name of the school to update.
        topics: List of strings representing the updated topics for the school.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
