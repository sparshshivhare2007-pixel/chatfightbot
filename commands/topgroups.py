import html
from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.enums import ParseMode
import database as db
from ui.keyboards import topgroups_keyboard


# =========================
# Generate Top Groups Text
# =========================

def generate_top_groups(mode="overall"):

    data = db.get_top_groups(mode)

    if not data:
        return None

    text = f"🏆 <b>TOP GROUPS ({mode.upper()})</b>\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, (group_id, total) in enumerate(data, start=1):

        group_info = db.get_group_info(group_id)
        title = group_info.get("title", "Group") if group_info else "Group"

        safe_title = html.escape(title)
        medal = medals[i - 1] if i <= 3 else f"{i}."

        text += f"{medal} {safe_title} • <b>{total}</b>\n"

    return text


# =========================
# Command
# =========================

async def topgroups_cmd(client, message):

    mode = "overall"

    text = generate_top_groups(mode)

    if not text:
        await message.reply("📊 No ranking data found.")
        return

    await message.reply(
        text,
        reply_markup=topgroups_keyboard(mode),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# =========================
# Callback (Fast Switching)
# =========================

async def topgroups_callback(client, callback_query):

    try:
        await callback_query.answer()
    except:
        return

    try:
        _, mode = callback_query.data.split(":")
    except:
        return

    text = generate_top_groups(mode)

    if not text:
        await callback_query.message.edit_text("📊 No ranking data found.")
        return

    await callback_query.message.edit_text(
        text,
        reply_markup=topgroups_keyboard(mode),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# =========================
# Handlers
# =========================

topgroups_handler = MessageHandler(
    topgroups_cmd,
    filters.command("topgroups")
)

topgroups_callback_handler = CallbackQueryHandler(
    topgroups_callback,
    filters.regex("^topgroups:")
)
