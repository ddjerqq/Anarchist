import disnake
from disnake.ext import commands
from disnake.ext import tasks

from database import database
from utils import *
from __main__ import GUILD_IDS, STATUSES


class EventsAndTasks(commands.Cog):
    def __init__(self, client: commands.bot.Bot):
        self.client = client
        self.save_database.start()
        self.status_cycle.start()

    @commands.Cog.listener()
    async def on_ready(self):
        old_user_count = len(database.users)
        for guild in self.client.guilds:
            rgb(f"[========== ", 0xffff00, newline=False)
            rgb(guild.name, 0xffffff, newline=False)
            rgb(f" ==========]", 0xffff00)
            async for member in guild.fetch_members(limit=None):
                if member.bot: continue
                if member.id not in database:
                    database.add_user(member.id, member.name)

                tmp_user = database[member.id]
                if tmp_user.name != member.name:
                    rgb(f"[^] {database[member.id].name}'s name updated to {member.name}", 0xffff00)
                    database[member.id].name = member.name

        rgb(f"[+] added {len(database.users) - old_user_count} new users", 0xffff00)
        rgb("[*] Bot is online", 0x00ff00)

    @tasks.loop(seconds=10)
    async def status_cycle(self):
        await self.client.change_presence(
            activity = disnake.Activity(
                type = disnake.ActivityType.playing,
                name = next(STATUSES)
            )
        )

    @status_cycle.before_loop
    async def before_status_cycle(self):
        await self.client.wait_until_ready()

    @tasks.loop(seconds=300)
    async def save_database(self):
        database._save()

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

        em = disnake.Embed(color=0xFF0000, title="unhandled error")
        em.add_field(name="error:", value=error, inline=False)

        await ctx.send(embed=em)

        warn(error)
        print(type(error))

    @commands.Cog.listener()
    async def on_slash_command_error( self, inter: disnake.ApplicationCommandInteraction, error ):
        if isinstance(error, commands.errors.CommandOnCooldown):
            return

        em = disnake.Embed(color=0xFF0000, title="unhandled error")
        em.add_field(name="error:", value=error, inline=False)

        await inter.send(embed=em)

        warn(error)
        print(type(error))

    @commands.Cog.listener()
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            em = disnake.Embed(
                color=0xFF0000, 
                title="Error",
                description="Bot do not have balances, dummy")
            await inter.send(embed=em)
        else:
            em = disnake.Embed(
                color=0xFF0000, 
                title="Unhandled error",
                description=error)
            await inter.send(embed=em)
        warn(error)
        print(type(error))

def setup(client: disnake.Client):
    client.add_cog(EventsAndTasks(client))
