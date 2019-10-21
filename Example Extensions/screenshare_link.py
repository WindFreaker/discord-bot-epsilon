from discord.ext import commands


@commands.command()
@commands.guild_only()
async def screenshare(ctx):
    state = ctx.author.voice
    if state is not None:
        link = '<https://www.discordapp.com/channels/' + str(state.channel.guild.id) + '/' + str(state.channel.id) + '>'
        await ctx.send('Click this link: ' + link)
    else:
        await ctx.send('You are currently not in a voice channel')


def setup(bot):
    bot.add_command(screenshare)
