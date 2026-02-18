from database.connection import db

async def update_global(user_id):
    await db.users.update_one(
        {"user_id": user_id},
        {"$inc": {"count": 1}},
        upsert=True
    )
