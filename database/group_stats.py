from database.connection import db

async def update_group(group_id):
    await db.groups.update_one(
        {"group_id": group_id},
        {"$inc": {"count": 1}},
        upsert=True
    )
