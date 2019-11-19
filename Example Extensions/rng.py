from discord.ext import commands
import random

from messenger import Messenger


@commands.command()
async def roll(ctx, *arg):
    try:
        limit = 20
        if len(arg) != 0:
            limit = int(arg[0])
        results = random.randint(0, limit) + 1
        await Messenger(ctx, 'You rolled a ' + str(results)).success()
    except ValueError:
        await Messenger(ctx, f'The parameter `{arg[0]}` is not a positive integer').error()


def setup(bot):
    bot.add_command(roll)
