#!/usr/bin/env python3
"""
Provides statistics about Nginx logs stored in MongoDB.
Provides top 10 most present IP Addresses
"""

from pymongo import MongoClient


def top_ips(logs_collection):
    """
    Returns the top 10 most present IP addresses in the logs collection.
    """

    count = logs_collection.count_documents({})
    print("{} logs".format(count))
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        meth_count = logs_collection.count_documents(
            {"method": {
                "$eq": method
            }})
        print("\tmethod {}: {}".format(method, meth_count))

    status_checks = logs_collection.count_documents(
        {"$and": [{
            "method": {
                "$eq": 'GET'
            }
        }, {
            "path": "/status"
        }]})
    print("{} status check".format(status_checks))

    top_ips = logs_collection.aggregate([{
        "$group": {
            "_id": "$ip",
            "count": {
                "$sum": 1
            }
        }
    }, {
        '$sort': {
            "count": -1
        }
    }, {
        "$limit": 10
    }])

    print("IPs:")
    top_ip_list = []
    for doc in top_ips:
        top_ip_list.append((doc.get("_id"), doc.get("count")))
    return top_ip_list


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    top_ips(logs_collection)
