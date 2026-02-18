from pyrogram.handlers import CallbackQueryHandler
from callbacks.rankings_toggle import handle_ranking_toggle

async def callback_router(client, callback_query):
    data = callback_query.data

    if data.startswith("rank:"):
        await handle_ranking_toggle(client, callback_query)

callback_handler = CallbackQueryHandler(callback_router)
