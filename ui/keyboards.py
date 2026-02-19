from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ranking_keyboard(mode: str, scope: str, target_id: int):

    def button(text: str, key: str):

        is_active = key == mode

        return InlineKeyboardButton(
            text=f"{'🟢' if is_active else '⚪'} {text}",
            callback_data=f"rank:{scope}:{key}:{target_id}"
        )

    return InlineKeyboardMarkup([
        [
            button("Overall", "overall"),
            button("Today", "today"),
            button("Week", "week")
        ]
    ])
