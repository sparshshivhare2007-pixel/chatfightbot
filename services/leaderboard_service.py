from database.connection import db
from datetime import datetime, timedelta


async def get_group_top(group_id, mode):

    query = {"group_id": group_id}

    if mode == "today":
        today = datetime.utcnow().strftime("%Y-%m-%d")
        query["date"] = today

    elif mode == "week":
        week_ago = datetime.utcnow() - timedelta(days=7)
        query["date"] = {"$gte": week_ago.strftime("%Y-%m-%d")}

    pipeline = [
        {"$match": query},
        {
            "$group": {
                "_id": "$user_id",
                "total": {"$sum": "$count"}
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ]

    result = db.messages.aggregate(pipeline)
    return [(doc["_id"], doc["total"]) async for doc in result]


async def get_global_top(mode):

    query = {}

    if mode == "today":
        today = datetime.utcnow().strftime("%Y-%m-%d")
        query["date"] = today

    elif mode == "week":
        week_ago = datetime.utcnow() - timedelta(days=7)
        query["date"] = {"$gte": week_ago.strftime("%Y-%m-%d")}

    pipeline = [
        {"$match": query},
        {
            "$group": {
                "_id": "$user_id",
                "total": {"$sum": "$count"}
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ]

    result = db.messages.aggregate(pipeline)
    return [(doc["_id"], doc["total"]) async for doc in result]


async def get_top_groups(mode):

    query = {}

    if mode == "today":
        today = datetime.utcnow().strftime("%Y-%m-%d")
        query["date"] = today

    elif mode == "week":
        week_ago = datetime.utcnow() - timedelta(days=7)
        query["date"] = {"$gte": week_ago.strftime("%Y-%m-%d")}

    pipeline = [
        {"$match": query},
        {
            "$group": {
                "_id": "$group_id",
                "total": {"$sum": "$count"}
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ]

    result = db.messages.aggregate(pipeline)
    return [(doc["_id"], doc["total"]) async for doc in result]


async def get_user_groups(user_id):

    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$group_id",
                "total": {"$sum": "$count"}
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ]

    result = db.messages.aggregate(pipeline)
    return [(doc["_id"], doc["total"]) async for doc in result]
