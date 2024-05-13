#!/usr/bin/env python3
"""
Provides statistics about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Provides statistics about Nginx logs stored in MongoDB.

    Args:
        mongo_collection: pymongo collection object
        representing the MongoDB collection.

    Returns:
        None. Prints the statistics to the console.
    """
    # Total number of logs
    total_logs = mongo_collection.count_documents({})

    print(f"{total_logs} logs")

    # Count of different HTTP methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = mongo_collection.count_documents({"method": method})
        print(f"    method {method}: {method_count}")

    # Number of logs with method=GET and path=/status
    status_check_count = mongo_collection.count_documents(
                                                         {"method": "GET",
                                                          "path": "/status"}
                                                         )
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Access the desired collection
    log_collection = client.logs.nginx

    # Get statistics about the Nginx logs
    log_stats(log_collection)
