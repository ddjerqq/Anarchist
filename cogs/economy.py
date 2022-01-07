import discord
from discord.ext import commands

import time

from bot import PREFIX
from bot import database

from utils import *


class Economy(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    # Event
    # @commands.Cog.listener()
    # async def on_message(self):
    #    something idk

    # Command
    @commands.command(name="balance", aliases=["bal"])
    async def bal(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            member = ctx.author
        if member.id not in database:
            embed = discord.Embed(color=0xFF0000)
            embed.add_field(name="Error", value="could not find user by id")
            await ctx.reply(embed=embed)
            return
        embed = discord.Embed(color=0xFF0000)
        bank = database[member.id]["bank"]
        wallet = database[member.id]["wallet"]
        embed.add_field(
            name=f"{database[member.id]['name']}'s balance",
            value=f"**bank  :** {bank}\n**wallet:** {wallet}",
        )
        await ctx.send(embed=embed)

    @commands.command(name="work")
    @commands.cooldown(1, 30, commands.BucketType.User)
    async def work(self, ctx: commands.Context):
        id = ctx.author.id
        database.money_wallet(id, 10)
        tmp_user = database[id]
        tmp_user["last_work_time"] = time.time()
        database[id] = tmp_user
        await ctx.send("> you worked and earned 10 coins")
        database._save()

    # ------------------------------------------------------------------------------

    @commands.command()
    async def withdraw(self, ctx: commands.Context, amount) -> None:
        """
        withdraw any amount of money from your bank to you wallet
        """
        if amount == "max":
            bank = database[ctx.author.id]["bank"]
            if database.money_bank(ctx.author.id, -bank) == 1:
                database.money_wallet(ctx.author.id, bank)
                await ctx.send(f"> you withdrew {bank} from your bank account.")
                return
        else:
            amount = float(amount)

        if database[ctx.author.id]["bank"] - amount < -0.1:
            await ctx.send(f"> you do not have enough funds")
        else:
            if database.money_bank(ctx.author.id, -amount) == 1:
                database.money_wallet(ctx.author.id, amount)
                await ctx.send(f"> you withdrew {bank} from your bank account.")
        database._save()

    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "> missing required argument: amount\n> please specify the amount you want to withdraw from your wallet to your bank"
            )
        else:
            await ctx.send(error)

    # ------------------------------------------------------------------------------

    @commands.command()
    async def deposit(self, ctx: commands.Context, amount) -> None:
        """
        deposit money from your wallet to your bank account to keep it safe.
        """
        if amount == "max":
            wallet = database[ctx.author.id]["wallet"]
            if database.money_wallet(ctx.author.id, -wallet) == 1:
                database.money_bank(ctx.author.id, wallet)
                await ctx.send(f"> you deposited {wallet} to your bank account.")
                return
        else:
            amount = float(amount)

        if database[ctx.author.id]["wallet"] - amount < -0.1:
            await ctx.send(f"> you do not have enough funds")
        else:
            if database.money_wallet(ctx.author.id, -amount) == 1:
                database.money_bank(ctx.author.id, amount)
                await ctx.send(f"> depositted {amount} to your bank account")
        database._save()

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "> missing required argument: amount\n> please specify the amount you want to deposit"
            )
        else:
            await ctx.send(error)

    # ------------------------------------------------------------------------------


def setup(client):
    client.add_cog(Economy(client))
