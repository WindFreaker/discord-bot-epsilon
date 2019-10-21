from discord.ext import commands


@commands.Cog.listener()
async def on_message(message):
    if message.lower().find('@everyone') != -1 \
            and not message.author.permissions_in(message.channel).mention_everyone:
        await message.delete()
        await message.channel.send('Fuck you')


def setup(bot):
    bot.add_listener(on_message)
