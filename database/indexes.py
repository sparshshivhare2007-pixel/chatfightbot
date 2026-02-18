from database.connection import db

async def create_indexes():
    await db.users.create_index("user_id")
    await db.groups.create_index("group_id")
