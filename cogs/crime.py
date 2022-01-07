import discord
from discord.ext import commands

from bot import database
from bot import PREFIX

class Crime(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    # Event
    # @commands.Cog.listener()
    # async def on_message(self):
    #    something idk

    # Command
    #FIXME
    @commands.command()
    async def rob(self, ctx: commands.Context, id: str):
        id = id.split("!")[1].split(">")[0]

        if id in database:
            amount = database[id]["wallet"]
            database.money(id, -amount, bank=False)
            database.money(ctx.author.id, amount, bank=False)
            await ctx.send(f"> you successfully robbed <@!{id}> and stole {amount}")
        else:
            await ctx.send(f"> could not find user")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("> missing required argument: id\n> who are you robbing dumbass>?")
        else:
            await ctx.send(error)
    #----------------------------------------------------------------
    
    #FIXME
    @commands.command()
    async def kill(self, ctx: commands.Context, id: str):
        id = id.split("!")[1].split(">")[0]

        if id in database:
            wallet = database[id]["wallet"]
            bank   = database[id]["bank"]
            database.money(id, -wallet, bank=False)
            database.money(id, -bank,   bank=True)
            await ctx.send(f"> you successfully killed <@!{id}> their money has been reset, \nbut.. why.. would you, ever, do that..??")
        else:
            await ctx.send(f"> could not find user")
    
    @kill.error
    async def kill_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("> missing required argument: id\n> who are you killing dumbass>?")
        else:
            await ctx.send(error)
    #------------------------------------------------------------------------------

def setup(client):
    client.add_cog(Crime(client))