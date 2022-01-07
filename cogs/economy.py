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
    @commands.command()
    async def bal(self, ctx: commands.Context, id: str = None):
        if id == None:
            embed = discord.Embed( color=0xff0000 )
            bank   = database[ctx.author.id]['bank']
            wallet = database[ctx.author.id]['wallet']
            embed.add_field( name = f"{database[ctx.author.id]['name']}'s balance", value = f"**bank  :** {bank}\n**wallet:** {wallet}" )
        else:
            #get id from mention, if mention
            if id.startswith("<@!"): id = int( id.split("!")[1].split(">")[0] )
            embed = discord.Embed(color=0xff0000 )
            if id in database:
                bank   = database[id]['bank']
                wallet = database[id]['wallet']
                embed.add_field( name = f"{database[id]['name']}'s balance", value = f"**bank  :** {bank}\n**wallet:** {wallet}" )
            else:
                embed.add_field( name="Error", value="could not find user by id" )
        
        await ctx.send(embed=embed)

    @commands.command()
    async def work(self, ctx: commands.Context):
        id = ctx.author.id
        if time.time() - database[id]["last_work_time"] >= 60.0:
            database.money_wallet(id, 10)
            tmp_user = database[id]
            tmp_user["last_work_time"] = time.time()
            database[id] = tmp_user
            await ctx.send("> you worked and earned 10 coins")
        else:
            await ctx.send(f"> you worked in the past minute, you have to wait { round( 60 - ( time.time() - database[id]['last_work_time']) ) } seconds")
        database._save()
    #------------------------------------------------------------------------------

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
            await ctx.send("> missing required argument: amount\n> please specify the amount you want to withdraw from your wallet to your bank")
        else:
            await ctx.send(error)
    #------------------------------------------------------------------------------

    @commands.command()
    async def deposit(self, ctx: commands.Context, amount) -> None:
        """
            deposit money from your wallet to your bank account to keep it safe.
        """
        if amount == "max":
            wallet = database[ctx.author.id]['wallet']
            if database.money_wallet(ctx.author.id, -wallet) == 1:
                database.money_bank(ctx.author.id, wallet)
                await ctx.send(f"> you deposited {wallet} to your bank account.")
                return
        else:
            amount = float(amount)

        if database[ctx.author.id]['wallet'] - amount < -0.1:
            await ctx.send(f"> you do not have enough funds")
        else:
            if database.money_wallet(ctx.author.id, -amount) == 1:
                database.money_bank(ctx.author.id, amount)
                await ctx.send(f"> depositted {amount} to your bank account")
        database._save()

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("> missing required argument: amount\n> please specify the amount you want to deposit")
        else:
            await ctx.send(error)
    #------------------------------------------------------------------------------

def setup(client):
    client.add_cog(Economy(client))