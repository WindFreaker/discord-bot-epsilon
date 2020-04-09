import glob
import os
import discord
from discord.ext import commands
import critical_errors
import extension_dynamics
from database_handler import list_enabled_extensions
from dropbox_handler import download_extension

print(f'Library Version: {discord.__version__}')

bot = commands.Bot(command_prefix=commands.when_mentioned)  # TODO make this a config
bot.remove_command('help')  # TODO recreate help command but make it more useful
bot.add_cog(extension_dynamics.DynamicHandler(bot))

bot.owner_id = 132229650477744128  # hardcoded for WindFreaker#9893 TODO remove/change for better public use
critical_errors.setup(bot)

exts = list_enabled_extensions()
if len(exts) != 0:
    print('Downloading enabled extensions...')
    for ext in exts:
        download_extension(ext)

for file in glob.glob("extensions/*.py"):
    bot.load_extension('extensions.' + file[11:-3])
    # TODO - THIS NEEDS TO CHANGE
    # future versions of the bot should support enabling extensions on a per guild basis
    # currently all extensions are enabled without any guild specific checks


@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user} [{bot.user.id}] in the following guilds:')
    for guild in bot.guilds:
        print(f'{guild.name} [{guild.id}]')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='with databases!'))


bot.run(os.getenv('DISCORD_BOT_TOKEN'))
