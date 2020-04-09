bot_ref = None


def setup(bot):
    global bot_ref
    bot_ref = bot


async def dm_error_report(message):
    owner = bot_ref.get_user(bot_ref.owner_id)
    if owner.dm_channel is None:
        await owner.create_dm()
    await owner.dm_channel.send(message)
