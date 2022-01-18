from itertools import cycle

import disnake
from disnake.ext import commands
from disnake.ext import tasks

from database import database
from utils import *
from __main__ import PREFIX

STATUSES = cycle([f"{PREFIX}help", "worlds first crypto bot", f"{PREFIX}bal"])


class EventsAndTasks(commands.Cog):
    def __init__(self, client: commands.bot.Bot):
        self.client = client
        self.save_database.start()
        self.status_cycle.start()

    @tasks.loop(seconds=10)
    async def status_cycle(self):
        await self.client.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.listening, name="a song"
            )
        )

    @status_cycle.before_loop
    async def before_status_cycle(self):
        await self.client.wait_until_ready()

    @tasks.loop(seconds=120)
    async def save_database(self):
        database._save()
        database.generate_csv()

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if member.bot:
            return
        if member.id not in database:
            database.add_user(member.id, member.name)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            return
        if isinstance(error, commands.errors.CommandNotFound):
            return

        embed = disnake.Embed(color=0xFF0000, title="unhandled error")
        embed.add_field(name="error:", value=error, inline=False)

        await ctx.send(embed=embed)

        warn(error)
        print(type(error))

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

        ok("Bot is online")


def setup(client: disnake.Client):
    client.add_cog(EventsAndTasks(client))
