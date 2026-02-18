from database.connection import db
from utils.logger import logger


async def create_indexes():
    try:
        await db.users.create_index(
            [("user_id", 1)],
            name="user_id_1",
            unique=True
        )

        await db.groups.create_index(
            [("group_id", 1)],
            name="group_id_1",
            unique=True
        )

        await db.user_groups.create_index(
            [("user_id", 1), ("group_id", 1)],
            name="user_group_compound",
            unique=True
        )

        logger.info("Indexes ensured successfully.")

    except Exception as e:
        logger.warning(f"Index creation skipped: {e}")
