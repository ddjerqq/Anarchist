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

    @commands.slash_command(
        name        = "rank", 
        aliases     = ["leaderboard"],
        description = "Get the top users in this server",
        guild_ids   = GUILD_IDS
        )
    async def _rank(self, inter: ApplicationCommandInteraction) -> None:
        users = []
        async for user in inter.guild.fetch_members(limit=None):
            if not user.bot:
                users.append(database[user.id])

        sorted_users = sorted(users, key=lambda x: x.amount, reverse=True)[0:10]

        embed = disnake.Embed(
            title=f"{inter.guild.name} leaderboard",
            color=0x00FF00,
        )
        for user_index in range(len(sorted_users)):
            embed.add_field(
                name=f"#{user_index + 1} {sorted_users[user_index].name}",
                value=str(sorted_users[user_index].amount) + " ⏣",
                inline=False,
            )
        await inter.send(embed=embed)

    @commands.slash_command(
        name        = "bal",
        aliases     = ["balanace"],
        description = f"Get your balance or someone else's",
        guild_ids   = GUILD_IDS
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


    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name        = "work",
        description = f"work and earn 50 coins, you can use this command every 30 seconds",
        guild_ids   = GUILD_IDS
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
                title       = f"You are on cooldown",
                description = f"try again in {round(_error.retry_after)} seconds"
            )
            await ctx.send(embed = em)
        else:
            rgb(_error, 0xff0000)


    @commands.slash_command(
        name        = "give",
        description = f"Give a user an amount",
        guild_ids   = GUILD_IDS
    )
    async def _give(self, inter: ApplicationCommandInteraction, user: disnake.Member,amount: int) -> None:
        async with inter.channel.typing():
            _id = user.id
            if int(amount) < 0:
                em = disnake.Embed(
                    color=0xFF0000, title=f"What are you trying to do here 🤨⁉"
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
