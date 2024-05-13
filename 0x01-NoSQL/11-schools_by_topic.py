#!/usr/bin/env python3
"""
A function to retrieve schools with a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve schools with a specific topic from the MongoDB collection.

    Args:
        mongo_collection: pymongo collection object
        representing the MongoDB collection.
        topic: String representing the topic to search for.

    Returns:
        A list of school documents that have the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))
