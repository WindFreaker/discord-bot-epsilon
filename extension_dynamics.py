from discord.ext import commands
from discord.ext.commands import ExtensionAlreadyLoaded, ExtensionNotLoaded, ExtensionNotFound
from dropbox.exceptions import ApiError
from messenger import Messenger
from dropbox_handler import download_extension
from database_handler import save_extension_state


class DynamicHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, arg):
        arg = arg.lower()  # fixes bug with enabling one extension multiple times via slightly different capitalization
        try:
            download_extension(arg)
            self.bot.load_extension('extensions.' + arg)
            save_extension_state(arg, True)
            await Messenger(ctx, f'Extension `{arg}.py` successfully enabled').success()
        except (ApiError, ExtensionNotFound):
            await Messenger(ctx, f'Extension `{arg}.py` failed to enable')\
                .add_desc('No extension by that name was found').error()
        except ExtensionAlreadyLoaded:
            await Messenger(ctx, f'Extension `{arg}.py` failed to enable')\
                .add_desc('That extension is already enabled').error()

    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, arg):
        arg = arg.lower()  # fixes bug with enabling one extension multiple times via slightly different capitalization
        try:
            self.bot.unload_extension('extensions.' + arg)
            save_extension_state(arg, False)
            await Messenger(ctx, f'Extension `{arg}.py` successfully disabled').success()
        except ExtensionNotLoaded:
            await Messenger(ctx, f'Extension `{arg}.py` failed to disable')\
                .add_desc('No extension by that name is currently running').error()

    # reloads (effectively a disable and immediate enable) to update the code being used by an extension
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, arg):
        try:
            download_extension(arg)
            self.bot.reload_extension('extensions.' + arg)
            await Messenger(ctx, f'Extension `{arg}.py` has been reloaded').success()
        except ExtensionNotLoaded:
            await Messenger(ctx, f'No extension called `{arg}.py` is currently running').error()

    # prints a readable list of all extensions enabled for the bot
    # TODO make the list not print out the name of hidden extensions
    @commands.command()
    @commands.is_owner()
    async def extensions(self, ctx):
        output = '`'
        for ext in self.bot.extensions:
            output += ext[11:] + '.py`\n`'
        await Messenger(ctx, 'List of currently enabled extensions').add_desc(output[:-1]).success()
