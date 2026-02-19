from database import (
    redis_client,
    update_user_group,
    update_group,
    update_global
)
from datetime import datetime


async def increment_counter(group_id: int, user_id: int):

    # Always store IDs as string in Redis
    group_id = str(group_id)
    user_id = str(user_id)

    now = datetime.utcnow()

    # =========================
    # OVERALL
    # =========================
    redis_client.zincrby(f"group:{group_id}:overall", 1, user_id)
    redis_client.zincrby("global:overall", 1, user_id)
    redis_client.zincrby("groups:overall", 1, group_id)

    # =========================
    # TODAY (Date Based)
    # =========================
    today_key = now.strftime("%Y-%m-%d")

    redis_client.zincrby(f"group:{group_id}:today:{today_key}", 1, user_id)
    redis_client.zincrby(f"global:today:{today_key}", 1, user_id)
    redis_client.zincrby(f"groups:today:{today_key}", 1, group_id)

    # =========================
    # WEEK (ISO Week Based)
    # =========================
    year, week, _ = now.isocalendar()
    week_key = f"{year}-W{week}"

    redis_client.zincrby(f"group:{group_id}:week:{week_key}", 1, user_id)
    redis_client.zincrby(f"global:week:{week_key}", 1, user_id)
    redis_client.zincrby(f"groups:week:{week_key}", 1, group_id)

    # =========================
    # Mongo Backup
    # =========================
    await update_user_group(user_id, group_id)
    await update_group(group_id)
    await update_global(user_id)
