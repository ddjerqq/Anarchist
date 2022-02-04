import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands
from disnake.ext.commands import errors

# from __main__ import PREFIX
from __main__ import GUILD_IDS
from easydb import database
from utils import *


class Jobs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.slash_command(
        name        = "work",
        description = f"work and earn 50 coins, you can use this command every minute",
        # guild_ids   = GUILD_IDS
    )
    async def _work(self, inter: Aci):
        async with inter.channel.typing():
            em = disnake.Embed(
                color = 0x00FF00, 
                title = f"Nice work!",
                description= "You earned 50 coins"
                )
            await inter.send(embed = em)
            database.give(924293465997705286, inter.author.id, 50)
            database.update()

    @_work.error
    async def _work_error(self, ctx: commands.Context, _error):
        if isinstance(_error, errors.CommandOnCooldown):
            em = disnake.Embed(
                color       = 0xFF0000,
                title       = f"You are on cooldown!",
                description = f"You can work again in {round(_error.retry_after)} seconds"
            )
            await ctx.send(embed = em)
        else:
            rgb(_error, 0xff0000)


    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.slash_command(
        name = "daily",
        description = "use this command to claim your daily amount of coins",
        guild_ids = GUILD_IDS
    )
    async def _daily(self, inter: Aci):
        async with inter.channel.typing():
            database.give(924293465997705286, inter.author.id, 500)
        em = disnake.Embed(
            color = 0x00ff00,
            title = "Daily",
            description = f"You received 500 coins"
        )
        await inter.send(embed = em)

    @_daily.error
    async def _daily_error(self, ctx: commands.Context, _error):
        if isinstance(_error, errors.CommandOnCooldown):
            em = disnake.Embed(
                color       = 0xFF0000,
                title       = f"You have already collected your daily coins!",
                description = f"You can collect again in {round(_error.retry_after) // 86400} days"
            )
            await ctx.send(embed = em)
        else:
            rgb(_error, 0xff0000)


def setup(client):
    client.add_cog(Jobs(client))
