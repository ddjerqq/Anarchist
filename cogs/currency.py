import disnake
from disnake.ext import commands
from disnake.ext.commands import errors

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

        sorted_users = sorted(users, key=lambda x: x["amount"], reverse=True)[0:10]

        embed = disnake.Embed(
            title=f"{ctx.guild.name} leaderboard",
            color=0x00FF00,
        )
        for user_index in range(len(sorted_users)):
            embed.add_field(
                name=f"#{user_index + 1} {sorted_users[user_index]['name']}",
                value=str(sorted_users[user_index]["amount"]) + " ⏣",
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command(
        name="bal",
        aliases=["balanace"],
        description="Allows a user to get their balance or the balance of another user\nUsage:\n    `.bal (user)` or `.bal`",
    )
    async def _balance(
        self, ctx: commands.Context, user: disnake.Member = None
    ) -> None:
        if not user:
            user = ctx.author
        _id = user.id

        embed = disnake.Embed(
            color=0x00FF00, title=f"{database[_id]['name']}'s balance"
        )
        embed.add_field(
            name="total amount", value=f"{database[_id]['amount']} ⏣", inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name="work")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _work(self, ctx: commands.Context) -> None:
        async with ctx.channel.typing():
            database.work(ctx.author.id)
            embed = disnake.Embed(color=0x00FF00, title=f"nice work! \nyou earned 25 ⏣")
            await ctx.send(embed=embed)

    @_work.error
    async def _work_error(self, ctx: commands.Context, _error) -> None:
        if isinstance(_error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                color=0xFF0000,
                title=f"slow down buddy, you're on cooldown\ntry again in {round(_error.retry_after)} seconds",
            )
            await ctx.send(embed=embed)
        else:
            warn(_error)

    @commands.command(name="give")
    async def _give(
        self, ctx: commands.Context, user: disnake.Member, amount: str
    ) -> None:
        async with ctx.channel.typing():
            _id = user.id
            if amount.lower() == "all" or amount.lower() == "max":
                amount = database[ctx.author.id]["amount"]
            else:
                if int(amount) > 0:
                    amount = int(amount)
                else:
                    embed = disnake.Embed(
                        color=0xFF0000, title=f"what are you trying to do here 🤨⁉"
                    )
                    await ctx.send(embed=embed)
                    return

        if database.give(ctx.author.id, _id, amount):
            embed = disnake.Embed(
                color=0x00FF00,
                title=f"you successfully gave {database[_id]['name']} {amount} ⏣",
            )
            # embed2 = disnake.Embed(
            #     color = 0xff0000,
            #     title = f"{database[ctx.author.id]['name']} gave you {amount} coins"
            #     )
            # await dm_user(_id, embed = embed2)
        else:
            embed = disnake.Embed(
                color=0xFF0000, title=f"you don't have enough money dumbass"
            )

        await ctx.send(embed=embed)

    @_give.error
    async def _give_error(self, ctx: commands.Context, _error) -> None:
        if isinstance(_error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                color=0xFF0000,
                title=f"slow down buddy, you're on cooldown\ntry again in {round(_error.retry_after)} seconds",
            )
            await ctx.send(embed=embed)
        else:
            warn(_error)


def setup(client):
    client.add_cog(Currency(client))
