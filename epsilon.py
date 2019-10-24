import glob
import os
import discord
from discord.ext import commands
import storage_handler
import dynamic_handler
from storage_handler import download_extension

print(f'Library Version: {discord.__version__}')
try:
    print('Epsilon Version: v0.' + os.getenv('HEROKU_RELEASE_VERSION')[1:])
except TypeError:
    print('Epsilon Version: [unknown environment]')

bot = commands.Bot(command_prefix=commands.when_mentioned)
bot.remove_command('help')
bot.add_cog(dynamic_handler.DynamicHandler(bot))

exts = storage_handler.read_config('startup')
if len(exts) != 0:
    print('Downloading extensions listed in startup.cfg ...')
    for ext in exts:
        download_extension(ext)

for file in glob.glob("extensions/*.py"):
    bot.load_extension('extensions.' + file[11:-3])


@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user} [{bot.user.id}] in the following guilds:')
    for guild in bot.guilds:
        print(f'{guild.name} [{guild.id}]')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='with python!'))


bot.run(os.getenv('DISCORD_BOT_TOKEN'))
