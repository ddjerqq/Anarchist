import disnake
from disnake.ext import commands

from database import database


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="blockchain")
    async def _blockchain(self, ctx: commands.Context):
        embed = disnake.Embed(title="is Blockchain valid?")

        if database.is_blockchain_valid:
            embed.description = "**Yes**"
            embed.color = 0x00FF00
        else:
            embed.description = "**No!!!**"
            embed.color = 0xFF0000

        await ctx.send(embed=embed)

    @commands.command(name="invite", aliases=["inv"])
    async def _invite(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Click me to Invite!",
            url="https://discord.com/api/oauth2/authorize?client_id=924293465997705286&permissions=8&scope=applications.commands%20bot",
        )
        embed.set_author(name=self.client.user, icon_url=self.client.user.avatar.url)
        await ctx.reply(embed=embed)


def setup(client: disnake.Client):
    client.add_cog(Information(client))