from pyrogram import filters
from pyrogram.handlers import MessageHandler
from services.leaderboard_service import get_top_groups
from ui.keyboards import ranking_keyboard
from services.formatting_service import format_leaderboard

async def topgroups_cmd(client, message):

    data = await get_top_groups("overall")
    text = await format_leaderboard(data, "TOP GROUPS")

    await message.reply(
        text,
        reply_markup=ranking_keyboard("overall", "groups", 0)
    )

topgroups_handler = MessageHandler(topgroups_cmd, filters.command("topgroups"))
