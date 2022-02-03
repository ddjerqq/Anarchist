import disnake
from disnake.ext import commands
from disnake.ext import tasks

from disnake import ApplicationCommandInteraction as Aci

from easydb import database
from utils import *
from __main__ import STATUSES
# from __main__ import GUILD_IDS


class EventsAndTasks(commands.Cog):
    def __init__(self, client: commands.bot.Bot):
        self.client = client
        self.save_database.start()
        self.status_cycle.start()

    @commands.Cog.listener()
    async def on_ready(self):
        new_user_count = 0
        for guild in self.client.guilds:
            rgb("[",   0xffffff, newline=False)
            rgb("===", 0xff0000, newline=False)
            rgb("] ",  0xffffff, newline = False)

            rgb(guild.name, 0xffffff)
            # noinspection PyTypeChecker
            async for member in guild.fetch_members(limit=None):
                if member.bot:
                    continue
                if member.id not in database:
                    database.add_user(member.id, member.name)
                    new_user_count += 1

                with database as c:
                    c.execute("""
                    SELECT username FROM users
                    WHERE id=?
                    """, (member.id,))
                    tmp_name = c.fetchone()[0]
                    if tmp_name != member.name:
                        c.execute("""
                        UPDATE users
                        SET username=?
                        WHERE id=?
                        """, (member.name, member.id))
                        rgb(f"[^] {tmp_name}'s name changed to {member.name}", 0xffff00)
                    else:
                        continue

        rgb(f"[+] added {new_user_count} new users", 0xffff00)
        del new_user_count
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

    @tasks.loop(seconds=30)
    async def save_database(self):
        database.update()

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
    async def on_slash_command_error(self, inter: Aci, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            return

        em = disnake.Embed(
            color=0xFF0000,
            title="unhandled error",
            description=str(error)
        )
        await inter.send(embed=em)

        warn(error)
        print(type(error))

    @commands.Cog.listener()
    async def on_user_command_error(self, inter: Aci, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            em = disnake.Embed(
                color=0xFF0000, 
                title="Error",
                description="Bots do not have balances, dummy")
            await inter.send(embed=em)
        else:
            em = disnake.Embed(
                color=0xFF0000, 
                title="Unhandled error",
                description=error)
            await inter.send(embed=em)
        warn(error)
        print(type(error))


def setup(client):
    client.add_cog(EventsAndTasks(client))
