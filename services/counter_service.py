from database import (
    redis_client,
    update_user_group,
    update_group,
    update_global
)


async def increment_counter(group_id, user_id):

    # Redis fast counters
    redis_client.zincrby(f"group:{group_id}:overall", 1, user_id)
    redis_client.zincrby(f"group:{group_id}:today", 1, user_id)
    redis_client.zincrby(f"group:{group_id}:week", 1, user_id)

    redis_client.zincrby("global:overall", 1, user_id)
    redis_client.zincrby("global:today", 1, user_id)
    redis_client.zincrby("global:week", 1, user_id)

    redis_client.zincrby("groups:overall", 1, group_id)
    redis_client.zincrby("groups:today", 1, group_id)
    redis_client.zincrby("groups:week", 1, group_id)

    # Mongo backup
    await update_user_group(user_id, group_id)
    await update_group(group_id)
    await update_global(user_id)
