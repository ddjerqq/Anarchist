from itertools import cycle

import discord
from discord.ext import commands
from discord.ext import tasks

from database import database
from utils import *
from __main__ import PREFIX

STATUSES = cycle( [f"{PREFIX}help", "worlds first crypto bot", f"{PREFIX}bal"] )

class Economy(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.save_database.start()
        self.status_cycle.start()

    @tasks.loop(seconds = 10)
    async def status_cycle(self):
        await self.client.change_presence( 
            activity = discord.Game(next(STATUSES))
            )

    @tasks.loop(seconds = 120)
    async def save_database(self):
        database._save()
        database.generate_csv()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot: return
        if member.id not in database:
            database.add_user(member.id, member.name)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        embed = discord.Embed(
            color = 0xff0000,
            title = "unhandled error"
            )
        embed.add_field(
            name   = "error:",
            value  = error,
            inline = False)

        await ctx.send(embed=embed)
        
        warn(error)
        print(type(error))

    @commands.Cog.listener()
    async def on_ready(self):
        old_user_count = len(database)
        for guild in self.client.guilds:
            async for member in guild.fetch_members(limit = None):
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

        await self.client.change_presence(activity=discord.Game(F"{PREFIX}help"))
        ok("Bot is online")

def setup(client: discord.Client):
    client.add_cog(Economy(client))