from __main__ import PREFIX
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from disnake.ext.commands import errors

from helpers.bot_helper import dm_user
from __main__ import GUILD_IDS
from database import database
from utils import *


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.slash_command(
        name        = "work",
        description = f"work and earn 50 coins, you can use this command every 30 seconds",
        #guild_ids   = GUILD_IDS
    )
    async def _work(self, inter: ApplicationCommandInteraction) -> None:
        async with inter.channel.typing():
            
            database.give("bank", inter.author.id, 50)

            em = disnake.Embed(
                color = 0x00FF00, 
                title = f"Nice work! \nYou earned 50 ⏣"
                )
            await inter.send(embed = em)

    @_work.error
    async def _work_error(self, ctx: commands.Context, _error) -> None:
        if isinstance(_error, errors.CommandOnCooldown):
            em = disnake.Embed(
                color       = 0xFF0000,
                title       = f"You are on cooldown!",
                description = f"You can work again in {round(_error.retry_after)} seconds"
            )
            await ctx.send(embed = em)
        else:
            rgb(_error, 0xff0000)

    @commands.slash_command(
        name        = "bal",
        aliases     = ["balanace"],
        description = f"Get your, or someone else's balance",
        #guild_ids   = GUILD_IDS
    )
    async def _balance(self, inter: ApplicationCommandInteraction, user: disnake.Member = None) -> None:
        if not user:
            user = inter.author
        _id = user.id

        em = disnake.Embed(
            color       = 0x00FF00, 
            title       = f"{database[_id].name}'s balance",
            description = f"{database[_id].amount} ⏣"
        )
        await inter.send(embed = em)

    @commands.slash_command(
        name        = "give",
        description = f"Give a user some coins, minimum transaction is 50 ⏣",
        #guild_ids   = GUILD_IDS
    )
    async def _give(self, inter: ApplicationCommandInteraction, user: disnake.Member, amount: int) -> None:
        async with inter.channel.typing():
            _id = user.id
            if int(amount) < 50:
                em = disnake.Embed(
                    color=0xFF0000, title=f"Minimum transaction is 50 ⏣"
                )
                await inter.send(embed = em)
                return

            if database.give(inter.author.id, _id, amount):
                em = disnake.Embed(
                    color=0x00FF00,
                    title=f"You successfully gave {database[_id].name} {amount} ⏣"
                )
                notificatoin_embed = disnake.Embed(
                    color = 0x00ff00,
                    title = f"{database[inter.author.id].name} gave you {amount} coins"
                    )
                if database[_id].notifications:
                    await user.send(embed = notificatoin_embed)

            else:
                em = disnake.Embed(
                    color=0xFF0000, title=f"You don't have enough money LMAOO"
                )

            await inter.send(embed = em)

    @_give.error
    async def _give_error(self, ctx: commands.Context, _error) -> None:
        if isinstance(_error, errors.MemberNotFound):
            embed = disnake.Embed(
                color=0xFF0000,
                title=f"/give or {PREFIX}give @member amount"
            )
            await ctx.send(embed=embed)
        else:
            rgb(_error, 0xff0000)

def setup(client):
    client.add_cog(Currency(client))
