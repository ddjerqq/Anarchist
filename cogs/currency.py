from __main__ import PREFIX
import disnake
from disnake.ext import commands
from disnake.ext.commands import errors

from helpers.bot_helper import dm_user
from database import database
from utils import *


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="rank", aliases=["leaderboard"])
    async def _rank(self, ctx: commands.Context) -> None:
        users = []
        async for user in ctx.guild.fetch_members(limit=None):
            if not user.bot:
                users.append(database[user.id])

        sorted_users = sorted(users, key=lambda x: x.amount, reverse=True)[0:10]

        embed = disnake.Embed(
            title=f"{ctx.guild.name} leaderboard",
            color=0x00FF00,
        )
        for user_index in range(len(sorted_users)):
            embed.add_field(
                name=f"#{user_index + 1} {sorted_users[user_index].name}",
                value=str(sorted_users[user_index].amount) + " ⏣",
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command(
        name="bal",
        aliases=["balanace"],
        description=f"Allows a user to get their balance or the balance of another user\nUsage:\n    `{PREFIX}bal (user)` or `{PREFIX}bal`",
    )
    async def _balance(self, ctx: commands.Context, user: disnake.Member = None) -> None:
        if not user:
            user = ctx.author
        _id = user.id

        embed = disnake.Embed(
            color=0x00FF00, title=f"{database[_id].name}'s balance"
        )
        embed.add_field(
            name="total amount", 
            value=f"{database[_id].amount} ⏣", 
            inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(name="work")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _work(self, ctx: commands.Context) -> None:
        async with ctx.channel.typing():
            database.give("bank", ctx.author.id, 50)
            embed = disnake.Embed(
                color=0x00FF00, 
                title=f"Nice work! \nYou earned 25 ⏣")
            await ctx.send(embed=embed)

    @_work.error
    async def _work_error(self, ctx: commands.Context, _error) -> None:
        if isinstance(_error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                color=0xFF0000,
                title=f"You are on cooldown\ntry again in {round(_error.retry_after)} seconds"
            )
            await ctx.send(embed=embed)
        else:
            warn(_error)

    @commands.command(name="give")
    async def _give(self, ctx: commands.Context, user: disnake.Member, amount: int) -> None:    
        async with ctx.channel.typing():
            _id = user.id
            
            if int(amount) < 0:
                embed = disnake.Embed(
                    color=0xFF0000, title=f"What are you trying to do here 🤨⁉"
                )
                await ctx.send(embed=embed)
                return

            if database.give(ctx.author.id, _id, amount):
                embed = disnake.Embed(
                    color=0x00FF00,
                    title=f"You successfully gave {database[_id].name} {amount} ⏣"
                )
                embed2 = disnake.Embed(
                    color = 0xff0000,
                    title = f"{database[ctx.author.id].name} gave you {amount} coins"
                    )
                if database[_id].notifications:
                    await dm_user(_id, embed = embed2)

            else:
                embed = disnake.Embed(
                    color=0xFF0000, title=f"You don't have enough money LMAOO"
                )

            await ctx.send(embed=embed)

    @_give.error
    async def _give_error(self, ctx: commands.Context, _error) -> None:
        if isinstance(_error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                color=0xFF0000,
                title=f"You're on cooldown\nTry again in {round(_error.retry_after)} seconds",
            )
            await ctx.send(embed=embed)
        elif isinstance(_error, errors.MemberNotFound):
            embed = disnake.Embed(
                color=0xFF0000,
                title=f"{PREFIX}give @member amount"
            )
            await ctx.send(embed=embed)
        else:
            warn(_error)


def setup(client):
    client.add_cog(Currency(client))
