from services.leaderboard_service import (
    get_group_top,
    get_global_top,
    get_top_groups
)
from services.formatting_service import format_leaderboard
from ui.keyboards import ranking_keyboard


async def handle_ranking_toggle(client, callback_query):
    data = callback_query.data.split(":")
    # rank:scope:mode:id
    _, scope, mode, target_id = data

    target_id = int(target_id)

    if scope == "group":
        leaderboard = await get_group_top(target_id, mode)
        title = "LEADERBOARD"
    elif scope == "global":
        leaderboard = await get_global_top(mode)
        title = "GLOBAL LEADERBOARD"
    else:
        leaderboard = await get_top_groups(mode)
        title = "TOP GROUPS"

    text = await format_leaderboard(leaderboard, title)

    await callback_query.message.edit_text(
        text,
        reply_markup=ranking_keyboard(mode, scope, target_id)
    )

    await callback_query.answer()
