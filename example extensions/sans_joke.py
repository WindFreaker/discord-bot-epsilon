from discord.ext import commands


def sans_check(message):
    result = message.lower().find('sans')
    if result != -1:
        return True
    return False


@commands.Cog.listener()
async def on_message(message):
    if sans_check(message.content) and message.guild is not None \
            and message.guild.me not in message.mentions and not message.author.bot:
        await message.channel.send('table')


def setup(bot):
    bot.add_listener(on_message)
