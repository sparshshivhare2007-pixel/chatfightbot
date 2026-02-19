from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================
# GROUP LEADERBOARD BUTTONS
# =========================

def ranking_keyboard(mode: str, scope: str, target_id: int):

    def button(text: str, key: str):
        active = key == mode

        return InlineKeyboardButton(
            text=f"{'🟢' if active else '⚪'} {text}",
            callback_data=f"rank:{scope}:{key}:{target_id}"
        )

    return InlineKeyboardMarkup([
        [
            button("Overall", "overall"),
            button("Today", "today"),
            button("Week", "week")
        ]
    ])


# =========================
# GLOBAL LEADERBOARD BUTTONS
# =========================

def global_ranking_keyboard(mode: str):

    def button(text: str, key: str):
        active = key == mode

        return InlineKeyboardButton(
            text=f"{'🟢' if active else '⚪'} {text}",
            callback_data=f"globalrank:{key}"
        )

    return InlineKeyboardMarkup([
        [
            button("Overall", "overall"),
            button("Today", "today"),
            button("Week", "week")
        ]
    ])
