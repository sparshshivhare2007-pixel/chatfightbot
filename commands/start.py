from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# IMAGES
# =========================

START_IMAGE = "https://files.catbox.moe/sscl7n.jpg"
SETTINGS_IMAGE = "https://files.catbox.moe/sscl7n.jpg"

SUPPORT_LINK = "https://t.me/Newchatfightsupport"


# =========================
# START COMMAND
# =========================

async def start_cmd(client, message):

    text = (
        "🤖 Welcome, this bot counts group messages and creates rankings.\n\n"
        "Add the bot to a group and start chatting."
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "➕ Add me in a group",
            url=f"https://t.me/{client.me.username}?startgroup=true"
        )],
        [InlineKeyboardButton("⚙ Settings", callback_data="settings"),
         InlineKeyboardButton("📊 Your stats", callback_data="mystats")]
    ])

    await message.reply_photo(
        photo=START_IMAGE,
        caption=text,
        reply_markup=buttons
    )


# =========================
# SETTINGS CALLBACK
# =========================

async def settings_callback(client, callback_query):

    await callback_query.answer()

    text = "⚙ <b>Bot Settings</b>\n\nChoose an option below."

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛟 Support Group", url=SUPPORT_LINK)],
        [InlineKeyboardButton("⬅ Back", callback_data="back_start")]
    ])

    await callback_query.message.delete()

    # IMPORTANT: parse_mode removed (Client already has HTML mode)
    await callback_query.message.reply_photo(
        photo=SETTINGS_IMAGE,
        caption=text,
        reply_markup=buttons
    )


# =========================
# BACK TO START
# =========================

async def back_start_callback(client, callback_query):

    await callback_query.answer()

    text = (
        "🤖 Welcome, this bot counts group messages and creates rankings.\n\n"
        "Add the bot to a group and start chatting."
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "➕ Add me in a group",
            url=f"https://t.me/{client.me.username}?startgroup=true"
        )],
        [InlineKeyboardButton("⚙ Settings", callback_data="settings"),
         InlineKeyboardButton("📊 Your stats", callback_data="mystats")]
    ])

    await callback_query.message.delete()

    await callback_query.message.reply_photo(
        photo=START_IMAGE,
        caption=text,
        reply_markup=buttons
    )


# =========================
# HANDLERS
# =========================

start_handler = MessageHandler(start_cmd, filters.command("start"))

settings_handler = CallbackQueryHandler(
    settings_callback,
    filters.regex("^settings$")
)

back_handler = CallbackQueryHandler(
    back_start_callback,
    filters.regex("^back_start$")
)
