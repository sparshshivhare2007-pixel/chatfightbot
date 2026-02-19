import html
from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.enums import ChatType, ParseMode
import database as db
from ui.keyboards import ranking_keyboard


# =========================
# Helper: Build Clickable Name
# =========================

def build_name(user_id, user_info):

    if not user_info:
        return "User"

    full_name = user_info.get("full_name") or "User"
    safe_name = html.escape(full_name)

    return f"<a href='tg://user?id={user_id}'>{safe_name}</a>"


# =========================
# Helper: Generate Leaderboard Text
# =========================

def generate_leaderboard(group_id: int, mode: str):

    data = db.get_leaderboard(group_id, mode)

    if not data:
        return None

    text = f"🏆 <b>GROUP LEADERBOARD ({mode.upper()})</b>\n\n"

    medals = ["🥇", "🥈", "🥉"]
    total_messages = 0

    for i, (user_id, total) in enumerate(data, start=1):

        user_info = db.get_user_info(user_id)
        name = build_name(user_id, user_info)

        medal = medals[i - 1] if i <= 3 else f"{i}."

        text += f"{medal} {name} • <b>{total}</b>\n"

        total_messages += total

    text += f"\n✉️ Total messages: <b>{total_messages}</b>"

    return text


# =========================
# /rankings Command
# =========================

async def rankings_cmd(client, message):

    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply("❌ This command works only in groups.")
        return

    group_id = message.chat.id
    mode = "overall"

    text = generate_leaderboard(group_id, mode)

    if not text:
        await message.reply("📊 No ranking data found.")
        return

    await message.reply(
        text,
        reply_markup=ranking_keyboard(mode, "group", group_id),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# =========================
# Callback Switching
# =========================

async def rankings_callback(client, callback_query):

    await callback_query.answer()

    try:
        _, scope, mode, target_id = callback_query.data.split(":")
        group_id = int(target_id)
    except Exception:
        return

    text = generate_leaderboard(group_id, mode)

    if not text:
        await callback_query.message.edit_text("📊 No ranking data found.")
        return

    await callback_query.message.edit_text(
        text,
        reply_markup=ranking_keyboard(mode, scope, group_id),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# =========================
# Handlers
# =========================

rankings_handler = MessageHandler(
    rankings_cmd,
    filters.command("rankings")
)

rankings_callback_handler = CallbackQueryHandler(
    rankings_callback,
    filters.regex("^rank:")
)
