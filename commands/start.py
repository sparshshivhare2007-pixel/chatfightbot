from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start_cmd(client, message):

    text = (
        "🤖 Welcome, this bot counts group messages and creates rankings.\n\n"
        "Add the bot to a group and start chatting."
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add me in a group", url="https://t.me/{}".format(client.me.username))],
        [InlineKeyboardButton("⚙ Settings", callback_data="settings"),
         InlineKeyboardButton("📊 Your stats", callback_data="mystats")]
    ])

    await message.reply(text, reply_markup=buttons)

start_handler = MessageHandler(start_cmd, filters.command("start"))
