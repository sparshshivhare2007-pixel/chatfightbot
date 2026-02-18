from database.connection import redis_client


async def reset_today():
    keys = await redis_client.keys("*:today")
    for key in keys:
        await redis_client.delete(key)


async def reset_week():
    keys = await redis_client.keys("*:week")
    for key in keys:
        await redis_client.delete(key)
