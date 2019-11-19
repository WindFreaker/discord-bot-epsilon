from discord.ext import commands
from discord.ext.commands import ExtensionAlreadyLoaded, ExtensionNotLoaded, ExtensionNotFound
from dropbox.exceptions import ApiError
from messenger import Messenger
from dropbox_handler import download_extension, edit_config


class DynamicHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, arg):
        try:
            download_extension(arg)
            self.bot.load_extension('extensions.' + arg)
            await Messenger(ctx, f'Extension `{arg}.py` has been enabled').success()
            edit_config('startup', arg)  # should always add arg from startup.cfg
        except (ApiError, ExtensionNotFound):
            await Messenger(ctx, f'Extension `{arg}.py` cannot be found').error()
        except ExtensionAlreadyLoaded:
            await Messenger(ctx, f'Extension `{arg}.py` is already enabled').error()

    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, arg):
        try:
            self.bot.unload_extension('extensions.' + arg)
            await Messenger(ctx, f'Extension `{arg}.py` has been disabled').success()
            edit_config('startup', arg)  # should always remove arg from startup.cfg
        except ExtensionNotLoaded:
            await Messenger(ctx, f'No extension called `{arg}.py` is currently enabled').error()

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, arg):
        try:
            download_extension(arg)
            self.bot.reload_extension('extensions.' + arg)
            await Messenger(ctx, f'Extension `{arg}.py` has been reloaded').success()
        except ExtensionNotLoaded:
            await Messenger(ctx, f'No extension called `{arg}.py` is currently running').error()

    @commands.command()
    @commands.is_owner()
    async def extensions(self, ctx):
        output = '`'
        for ext in self.bot.extensions:
            output += ext[11:] + '.py`\n`'
        await Messenger(ctx, 'List of currently enabled extensions').add_desc(output[:-1]).success()
