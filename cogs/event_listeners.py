import discord
from discord.ext import commands
from database import database
from discord.ext import tasks
from utils import *

PREFIX = "."


class EventListeners(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        old_user_count = len(database)
        for guild in self.client.guilds:
            async for member in guild.fetch_members(limit=None):
                if member.bot:
                    continue
                if member.id not in database:
                    database.add_user(member.id, member.name)
                else:
                    tmp_user = database[member.id]
                    if tmp_user["name"] != member.name:
                        old_name = tmp_user["name"]
                        tmp_user["name"] = member.name
                        database[member.id] = tmp_user
                        warn(f"{old_name}'s name updated to {tmp_user['name']}")

        warn(f"added {len(database) - old_user_count} new users")

        await self.client.change_presence(activity=discord.Game(f"{PREFIX}help"))
        ok("Bot is online")

    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        embed = discord.Embed(color=0xFF0000, title="unhandled error")
        embed.add_field(name="error:", value=error, inline=False)
        await ctx.send(embed=embed)
        warn(error)

    @commands.Cog.listener()
    async def on_member_join(member):
        if member.bot:
            return
        if member.id not in database:
            database.add_user(member.id, member.name)


def setup(client):
    client.add_cog(EventListeners(client))
