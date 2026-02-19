import html
from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.enums import ParseMode
import database as db
from ui.keyboards import global_ranking_keyboard


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
# Generate Global Leaderboard
# =========================

def generate_global_leaderboard(mode="overall"):

    data = db.get_global_leaderboard(mode)

    if not data:
        return None

    text = f"🌍 <b>GLOBAL LEADERBOARD ({mode.upper()})</b>\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, (user_id, total) in enumerate(data, start=1):

        user_info = db.get_user_info(user_id)
        name = build_name(user_id, user_info)

        medal = medals[i - 1] if i <= 3 else f"{i}."

        text += f"{medal} {name} • <b>{total}</b>\n"

    return text


# =========================
# Command Handler
# =========================

async def topusers_cmd(client, message):

    mode = "overall"

    text = generate_global_leaderboard(mode)

    if not text:
        await message.reply("📊 No ranking data found.")
        return

    await message.reply(
        text,
        reply_markup=global_ranking_keyboard(mode),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# =========================
# Callback Handler (Fast Switching)
# =========================

async def topusers_callback(client, callback_query):

    await callback_query.answer()

    try:
        _, mode = callback_query.data.split(":")
    except Exception:
        return

    text = generate_global_leaderboard(mode)

    if not text:
        await callback_query.message.edit_text("📊 No ranking data found.")
        return

    await callback_query.message.edit_text(
        text,
        reply_markup=global_ranking_keyboard(mode),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# =========================
# Handlers
# =========================

topusers_handler = MessageHandler(
    topusers_cmd,
    filters.command("topusers")
)

topusers_callback_handler = CallbackQueryHandler(
    topusers_callback,
    filters.regex("^globalrank:")
)
