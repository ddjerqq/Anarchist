import discord
from discord.ext import commands

from main import database
from main import PREFIX


class Crime(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    # Event
    # @commands.Cog.listener()
    # async def on_message(self):
    #    something idk

    # Command
    @commands.command(name="rob")
    async def rob(self, ctx: commands.Context, member: discord.Member = None):

        if not member:
            await ctx.reply("who you tryna rob? the air?")
            return
        if member.id not in database:
            await ctx.send(f"> could not find user with id {member.id}")
            return
        amount = database[member.id]["wallet"]
        database.money_wallet(member.id, -amount)
        database.money_wallet(ctx.author.id, amount)
        await ctx.send(f"> you successfully robbed {member.mention} and stole {amount}")

    # ----------------------------------------------------------------


def setup(client):
    client.add_cog(Crime(client))
