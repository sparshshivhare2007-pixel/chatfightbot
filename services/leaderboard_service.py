from database.connection import redis_client
from database.user_stats import get_user_groups


async def get_group_top(group_id, mode):
    key = f"group:{group_id}:{mode}"
    return await redis_client.zrevrange(key, 0, 9, withscores=True)


async def get_global_top(mode):
    key = f"global:{mode}"
    return await redis_client.zrevrange(key, 0, 9, withscores=True)


async def get_top_groups(mode):
    key = f"groups:{mode}"
    return await redis_client.zrevrange(key, 0, 9, withscores=True)


async def get_user_groups(user_id):
    return await get_user_groups(user_id)
