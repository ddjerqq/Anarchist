import discord
from discord.ext import commands

from main import PREFIX
from database import Database

class Crime(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    # Event
    # @commands.Cog.listener()
    # async def on_message(self):
    #    something idk

    # Command
    @commands.command()
    async def rob(self, ctx: commands.Context, id: str):
        if "!" in id:
            #if someone mentioned someone using the ID
            id = id.split("!")[1].split(">")[0]
        else:
            pass
        with Database(verbose=True) as db:
            if id in db:
                amount = db[id]["wallet"]
                db.money_wallet(id, -amount)
                db.money_wallet(ctx.author.id, amount)
                await ctx.send(f"> you successfully robbed <@!{id}> and stole {amount}")
            else:
                await ctx.send(f"> could not find user with id {id}")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("> missing required argument: id\n> who are you robbing dumbass?")
        else:
            await ctx.send(error)
    #----------------------------------------------------------------

def setup(client):
    client.add_cog(Crime(client))