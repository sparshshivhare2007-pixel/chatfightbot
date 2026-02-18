def admin_only(func):
    async def wrapper(client, message):
        if message.from_user.id != 123456789:
            return
        return await func(client, message)
    return wrapper
