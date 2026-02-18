from database import (
    get_leaderboard,
    get_global_leaderboard,
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
        leaderboard = get_leaderboard(target_id, mode)
        title = "GROUP LEADERBOARD"

    elif scope == "global":
        leaderboard = get_global_leaderboard(mode)
        title = "GLOBAL LEADERBOARD"

    else:  # groups
        leaderboard = get_top_groups(mode)
        title = "TOP GROUPS"

    text = await format_leaderboard(leaderboard, title)

    await callback_query.message.edit_text(
        text,
        reply_markup=ranking_keyboard(mode, scope, target_id)
    )

    await callback_query.answer()
