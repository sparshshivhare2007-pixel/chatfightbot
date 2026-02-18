from database import (
    get_leaderboard,
    get_global_leaderboard,
    get_user_groups_stats,
    get_top_groups as db_get_top_groups,
    get_user_info,
    get_group_info
)


# =========================
# GROUP LEADERBOARD
# =========================

async def get_group_top(group_id: int, mode: str):

    data = get_leaderboard(group_id, mode)

    result = []

    for user_id, total in data:
        user = get_user_info(user_id)
        name = user["full_name"] if user else "User"
        result.append((name, total))

    return result


# =========================
# GLOBAL LEADERBOARD
# =========================

async def get_global_top(mode: str):

    data = get_global_leaderboard(mode)

    result = []

    for user_id, total in data:
        user = get_user_info(user_id)
        name = user["full_name"] if user else "User"
        result.append((name, total))

    return result


# =========================
# USER GROUP STATS
# =========================

async def get_user_groups(client, user_id: int, mode="overall"):

    data = get_user_groups_stats(user_id, mode)

    result = []

    for group_id, total in data:
        group = get_group_info(group_id)
        title = group["title"] if group else "Group"
        result.append((title, total))

    return result


# =========================
# TOP GROUPS
# =========================

async def get_top_groups(mode: str):

    data = db_get_top_groups(mode)

    result = []

    for group_id, total in data:
        group = get_group_info(group_id)
        title = group["title"] if group else "Group"
        result.append((title, total))

    return result
