from database.connection import db
from datetime import datetime, timedelta


# ---------- Helper ----------
async def resolve_user(user_id):
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        return str(user_id)

    if user.get("username"):
        return f"@{user['username']}"

    return user.get("full_name", str(user_id))


async def resolve_group(group_id):
    group = await db.groups.find_one({"group_id": group_id})
    if not group:
        return str(group_id)

    return group.get("title", str(group_id))


# ---------- GROUP LEADERBOARD ----------
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

    result = []
    cursor = db.messages.aggregate(pipeline)

    async for doc in cursor:
        username = await resolve_user(doc["_id"])
        result.append((username, doc["total"]))

    return result


# ---------- GLOBAL USER LEADERBOARD ----------
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

    result = []
    cursor = db.messages.aggregate(pipeline)

    async for doc in cursor:
        username = await resolve_user(doc["_id"])
        result.append((username, doc["total"]))

    return result


# ---------- TOP GROUPS ----------
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

    result = []
    cursor = db.messages.aggregate(pipeline)

    async for doc in cursor:
        title = await resolve_group(doc["_id"])
        result.append((title, doc["total"]))

    return result


# ---------- MY TOP GROUPS ----------
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

    result = []
    cursor = db.messages.aggregate(pipeline)

    async for doc in cursor:
        title = await resolve_group(doc["_id"])
        result.append((title, doc["total"]))

    return result
