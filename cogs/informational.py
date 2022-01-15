import discord
from discord.ext import commands

from utils import *
from __main__ import PREFIX

from database import database

class Economy(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @commands.command(name = "rank", aliases = ["leaderboard"])
    async def _rank(ctx: commands.Context) -> None:
        users = []
        members = await ctx.guild.fetch_members( limit = None )
        [users.append(user) for user in members if not user.bot]
        
        sorted_users = sorted(users, key = lambda x: x["amount"], reverse = True)[0:10]

        embed = discord.Embed(
            title = f"{ctx.guild.name} leaderboard",
            color = 0xff0000,
        )
        for user_index in range(len(sorted_users)):
            embed.add_field(
                name   = f"#{user_index + 1} {sorted_users[user_index]['name']}",
                value  = str(sorted_users[user_index]["amount"]) + " ⏣",
                inline = False 
            )
        await ctx.send( embed = embed)



def setup(client: discord.Client):
    client.add_cog(Economy(client))