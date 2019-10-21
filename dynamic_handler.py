from discord.ext import commands
from discord.ext.commands import ExtensionAlreadyLoaded, ExtensionNotLoaded, ExtensionNotFound
from dropbox.exceptions import ApiError

from storage_handler import download_extension


class DynamicHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, arg):
        try:
            self.bot.load_extension('extensions.' + arg)
            await ctx.send('```Extension enabled```')
        except ExtensionNotFound:
            try:
                download_extension(arg)
                self.bot.load_extension('extensions.' + arg)
                await ctx.send('```Extension downloaded and enabled```')
            except ApiError:
                await ctx.send('```Extension not found```')
        except ExtensionAlreadyLoaded:
            await ctx.send('```Extension already enabled```')

    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, arg):
        try:
            self.bot.unload_extension('extensions.' + arg)
            await ctx.send('```extension disabled```')
        except ExtensionNotLoaded:
            await ctx.send('```Extension not already enabled```')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, arg):
        try:
            self.bot.reload_extension('extensions.' + arg)
            await ctx.send('```extension reloaded```')
        except ExtensionNotLoaded:
            await ctx.send('```Extension not already enabled```')

    @commands.command()
    @commands.is_owner()
    async def extensions(self, ctx):
        output = '```\n'
        for ext in self.bot.extensions:
            output += ext[11:] + '\n'
        await ctx.send(output + '```')
