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
            await ctx.send( f"<@{ctx.author.id}>'s balance \n> wallet: {database[ctx.author.id]['wallet']}\n > bank: {database[ctx.author.id]['bank']}\n" )
        else:
            #get id if mention
            if id.startswith("<@!"):
                id = int( id.split("!")[1].split(">")[0] )

            if id in database:
                await ctx.send( f"<@{id}>'s balance \n> wallet: {database[id]['wallet']}\n > bank: {database[id]['bank']}" )
            else:
                await ctx.send(f"> could not find user by id {id}")

    @commands.command()
    async def work(self, ctx: commands.Context):
        id = ctx.author.id
        if time.time() - database[id]["last_work_time"] >= 60.0:
            tmp_user = database[id]
            tmp_user["wallet"] += 10
            tmp_user["last_work_time"] = time.time()
            database[id] = tmp_user
            database._save() #TODO maybe we dont need to save this here
            await ctx.send("> you worked and earned 10 coins")
        else:
            await ctx.send(f"> you worked in the past minute, you have to wait { round(time.time() - float(database[id]['last_work_time']) ) }")            
    #------------------------------------------------------------------------------

    #FIXME
    @commands.command()
    async def withdraw(self, ctx: commands.Context, amount: int):
        """
            withdraw any amount of money from your bank to you wallet
        """
        if ctx.author.id in database:
            if database.check_bank(ctx.author.id, amount):
                database.money(ctx.author.id, -amount, bank=True)
                database.money(ctx.author.id, amount, bank=False)
                await ctx.send(f"> withdrew {amount}")
            else:
                await ctx.send(f"> you do not have enough funds")
        else:
            await ctx.send(f"> you are not registered, register with {PREFIX}register")
        database.save()
    
    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("> missing required argument: amount\n> please specify the amount you want to withdraw")
        else:
            await ctx.send(error)
    #------------------------------------------------------------------------------

    #FIXME
    @commands.command()
    async def deposit(self, ctx: commands.Context, amount: int):
        """
            deposit money from your wallet to your bank account to keep it safe.
        """
        if ctx.author.id in database:
            if database.check_wallet(ctx.author.id, amount):
                database.money(ctx.author.id, amount,  bank=True)
                database.money(ctx.author.id, -amount, bank=False)
                await ctx.send(f"> depositted {amount}")
            else:
                await ctx.send(f"> you do not have enough funds")
        else:
            await ctx.send(f"> you are not registered, register with {PREFIX}register")
        database.save()

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("> missing required argument: amount\n> please specify the amount you want to deposit")
        else:
            await ctx.send(error)
    #------------------------------------------------------------------------------

def setup(client):
    client.add_cog(Economy(client))