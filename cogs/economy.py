import time

import discord
from discord.ext import commands

from main import PREFIX
from database import Database

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
        with Database(verbose=True) as db:
            if not member:
                member = ctx.author
            if member.id not in db:
                embed = discord.Embed(color=0xFF0000)
                embed.add_field(name="Error", value="could not find user by id")
                await ctx.reply(embed=embed)
                return
            embed = discord.Embed(color=0xFF0000)
            bank  = db[int(member.id)]["bank"]
            wallet = db[int(member.id)]["wallet"]
            embed.add_field(
                name=f"{db[int(member.id)]['name']}'s balance",
                value=f"**bank  :** {bank}\n**wallet:** {wallet}",
            )
            await ctx.send(embed=embed)

    @commands.command(name="work")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def work(self, ctx: commands.Context):
        with Database(verbose=True) as db:
            id = ctx.author.id
            db.money_wallet(id, 10)
            tmp_user = db[id]
            tmp_user["last_work_time"] = time.time()
            db[id] = tmp_user
            await ctx.send("> you worked and earned 10 coins")
            db._save()

    # ------------------------------------------------------------------------------

    @commands.command()
    async def withdraw(self, ctx: commands.Context, amount) -> None:
        """
        withdraw any amount of money from your bank to you wallet
        """
        with Database(verbose=True) as db:
            if amount == "max":
                bank = db[ctx.author.id]["bank"]
                if db.money_bank(ctx.author.id, -bank) == 1:
                    db.money_wallet(ctx.author.id, bank)
                    await ctx.send(f"> you withdrew {bank} from your bank account.")
                    return
            else:
                amount = float(amount)

            if db[ctx.author.id]["bank"] - amount < -0.1:
                await ctx.send(f"> you do not have enough funds")
            else:
                if db.money_bank(ctx.author.id, -amount) == 1:
                    db.money_wallet(ctx.author.id, amount)
                    await ctx.send(f"> you withdrew {bank} from your bank account.")
            db._save()

    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("> missing required argument: amount\n> please specify the amount you want to withdraw from your wallet to your bank" )
        else:
            await ctx.send(error)

    # ------------------------------------------------------------------------------

    @commands.command()
    async def deposit(self, ctx: commands.Context, amount) -> None:
        """
        deposit money from your wallet to your bank account to keep it safe.
        """
        with Database(verbose=True) as db:
            if amount == "max":
                wallet = db[ctx.author.id]["wallet"]
                if db.money_wallet(ctx.author.id, -wallet) == 1:
                    db.money_bank(ctx.author.id, wallet)
                    await ctx.send(f"> you deposited {wallet} to your bank account.")
                    return
            else:
                amount = float(amount)

            if db[ctx.author.id]["wallet"] - amount < -0.1:
                await ctx.send(f"> you do not have enough funds")
            else:
                if db.money_wallet(ctx.author.id, -amount) == 1:
                    db.money_bank(ctx.author.id, amount)
                    await ctx.send(f"> depositted {amount} to your bank account")
            db._save()

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