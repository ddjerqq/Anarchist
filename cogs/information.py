import disnake
from disnake.ext import commands

from database import database


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="info")
    async def _info(self, ctx: commands.Context, user: disnake.Member = None):
        if not user:
            user = ctx.author

        embed: disnake.Embed = disnake.Embed(
            title=f"{user.name}#{user.discriminator}'s info", color=0x00FF00
        )
        embed.add_field(name="creation time", value=str(user.created_at), inline=False)
        embed.add_field(name="id", value=user.id, inline=False)
        embed.add_field(name="is bot?", value=user.bot, inline=False)
        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="blockchain")
    async def _blockchain(self, ctx: commands.Context):
        embed = disnake.Embed(title="BlockChain valid?")

        if database.is_blockchain_valid:
            embed.description = "**Yes**"
            embed.color = 0x00FF00
        else:
            embed.description = "**No**"
            embed.color = 0xFF0000

        await ctx.send(embed=embed)

    @commands.command(name="invite", aliases=["inv"])
    async def _invite(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Click me to Invite!",
            url="https://disnake.com/api/oauth2/authorize?client_id=924293465997705286&permissions=275884665968&scope=bot",
        )
        embed.set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed)


def setup(client: disnake.Client):
    client.add_cog(Information(client))
