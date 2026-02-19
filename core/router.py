from commands import start, rankings, topusers, topgroups, mytop, settings
from core.message_listener import message_counter
from core.callback_listener import callback_handler


def register_handlers(app):

    # =========================
    # COMMAND HANDLERS
    # =========================
    app.add_handler(start.start_handler)
    app.add_handler(rankings.rankings_handler)
    app.add_handler(topusers.topusers_handler)
    app.add_handler(topgroups.topgroups_handler)
    app.add_handler(mytop.mytop_handler)
    app.add_handler(settings.settings_handler)

    # =========================
    # CALLBACK HANDLERS
    # =========================
    app.add_handler(rankings.rankings_callback_handler)
    app.add_handler(topgroups.topgroups_callback_handler)
    app.add_handler(topusers.topusers_callback_handler)

    # Other callback handlers (settings, etc.)
    app.add_handler(callback_handler)

    # =========================
    # MESSAGE COUNTER
    # =========================
    app.add_handler(message_counter)
