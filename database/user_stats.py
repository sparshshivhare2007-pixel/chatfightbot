from database.connection import db

async def update_user_group(user_id, group_id):
    await db.user_groups.update_one(
        {"user_id": user_id, "group_id": group_id},
        {"$inc": {"count": 1}},
        upsert=True
    )

async def get_user_groups(user_id):
    cursor = db.user_groups.find({"user_id": user_id}).sort("count", -1).limit(10)
    return await cursor.to_list(length=10)
