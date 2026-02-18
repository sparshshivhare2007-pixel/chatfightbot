from database.connection import db
from datetime import datetime, timedelta
from pyrogram.errors import RPCError


# ---------- Resolve User (Live + Fallback) ----------
async def resolve_user(client, user_id):

    try:
        user = await client.get_users(user_id)

        if user.username:
            name = f"@{user.username}"
        else:
            name = user.first_name or str(user_id)

        return f"<a href='tg://user?id={user_id}'>{name}</a>"

    except RPCError:
        # Fallback Mongo
        user = await db.users.find_one({"user_id": user_id})
        if not user:
            return str(user_id)

        name = user.get("username") or user.get("full_name") or str(user_id)
        return f"<a href='tg://user?id={user_id}'>{name}</a>"


# ---------- Resolve Group (Live + Fallback) ----------
async def resolve_group(client, group_id):

    try:
        chat = await client.get_chat(group_id)
        return chat.title

    except:
        group = await db.groups.find_one({"group_id": group_id})
        if not group:
            return str(group_id)

        return group.get("title", str(group_id))


# ---------- GROUP LEADERBOARD ----------
async def get_group_top(client, group_id, mode):

    group_id = int(group_id)

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
        username = await resolve_user(client, doc["_id"])
        result.append((username, doc["total"]))

    return result


# ---------- GLOBAL USER LEADERBOARD ----------
async def get_global_top(client, mode):

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
        username = await resolve_user(client, doc["_id"])
        result.append((username, doc["total"]))

    return result


# ---------- TOP GROUPS ----------
async def get_top_groups(client, mode):

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
        title = await resolve_group(client, doc["_id"])
        result.append((title, doc["total"]))

    return result


# ---------- MY TOP GROUPS ----------
async def get_user_groups(client, user_id):

    user_id = int(user_id)

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
        title = await resolve_group(client, doc["_id"])
        result.append((title, doc["total"]))

    return result
