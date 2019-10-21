from discord.ext import commands
import random


@commands.command()
async def roll(ctx, *arg):
    try:
        limit = 20
        if len(arg) != 0:
            limit = int(arg[0])
        results = random.randint(0, limit) + 1
        await ctx.send('You rolled a ' + str(results))
    except ValueError:
        await ctx.send('The parameter `' + arg[0] + '` is not a positive integer')


def setup(bot):
    bot.add_command(roll)
