from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ranking_keyboard(mode, scope, target_id):

    def btn(text, m):
        if m == mode:
            return InlineKeyboardButton(
                f"🔘 {text}",
                callback_data=f"rank:{scope}:{m}:{target_id}"
            )
        return InlineKeyboardButton(
            text,
            callback_data=f"rank:{scope}:{m}:{target_id}"
        )

    return InlineKeyboardMarkup([
        [
            btn("Overall", "overall"),
            btn("Today", "today"),
            btn("Week", "week")
        ]
    ])
