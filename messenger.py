from discord import Embed, Color

success_color = Color.from_rgb(29, 185, 84)
error_color = Color.from_rgb(211, 68, 68)
unused_color = Color.from_rgb(108, 129, 203)


class Messenger:
    def __init__(self, ctx, title):
        self.channel = ctx.channel
        self.author = ctx.author
        self.title = title
        self.desc = None
        self.image = None

    def add_desc(self, description):
        self.desc = description
        return self

    def add_image(self, link):
        self.image = link
        return self

    async def success(self):
        embed = create_embed(success_color, self.author, self.title, self.desc, self.image)
        await self.channel.send(embed=embed)

    async def error(self):
        embed = create_embed(error_color, self.author, self.title, self.desc, self.image)
        await self.channel.send(embed=embed)


def create_embed(color, author, title, desc, image):
    embed = Embed(color=color, title=title, description=desc)
    if image is not None:
        embed.set_image(url=image)
    embed.set_footer(text=f'Request by {author.display_name} ({str(author)})')
    return embed
