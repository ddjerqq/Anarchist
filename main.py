# built-ins
import os

# ~~~~~~~~

# 3rd party libraries
import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle

# ~~~~~~~~~~~~~~~~~~~~~~~~

# local imports
from utils import *
from tokens import TOKEN
from database import Database

# ~~~~~~~~~~~~~~~~~~~~~~~

# globals
PREFIX = "."
client = commands.Bot(command_prefix = PREFIX, intents = discord.Intents.all())
client.remove_command("help")

database = Database(verbose=True)
# ~~~~~~~~~~~~~~~~~~~~~~~

@tasks.loop(seconds = 10)
async def change_status() -> None:
    statuses = cycle([f"{PREFIX}help", "My prefix is {PREFIX}", "rob anyone anytime 😈"])
    await client.change_presence(activity=discord.Game(next(statuses)))

@tasks.loop(seconds = 120)
async def save_database() -> None:
    database._save()
    database.generate_csv()

# events
@client.event
async def on_ready():
    # update member names in database
    for guild in client.guilds:
        async for member in guild.fetch_members(limit = None):
            if member.bot:
                continue
            if member.id not in database:
                database.add_user(member.id, member.name)
            else:
                tmp_user = database[member.id]
                if tmp_user["name"] != member.name:
                    tmp_user["name"] = member.name
                    database[member.id] = tmp_user
                    warn( f"{tmp_user['name']}'s name updated to {database[member.id]['name']}" )

    change_status.start()  # start loops
    save_database.start()
    ok("Bot is online")

@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed( color = 0xff0000, title="unhandled error" )
    embed.add_field( name = "error:", value = error, inline = False )
    await ctx.send( embed = embed )
    print(error)

# embed = discord.Embed( color = 0xff0000 )
# embed.add_field( name = "bank account", value = "bank money", inline = False )
# embed.add_field( name = "wallet account", value = "wallet money", inline = False )
# await ctx.send( embed = embed )

# commands

@client.command(name="bal", aliases = ["balanace"])
async def balance(ctx: commands.Context, _id: str = None) -> None:
    if _id == None:
        _id = ctx.author.id
    elif "@" in _id:
        #<@!923600698967461898>
        _id = int( _id[3:-1] )
    else:
        _id = int(_id)
    
    embed = discord.Embed( color = 0xff0000, title = f"{database[_id]['name']}'s balance" )
    embed.add_field( name = "bank account",   value = database[_id]["bank"],   inline = False )
    embed.add_field( name = "wallet account", value = database[_id]["wallet"], inline = False )
    await ctx.send( embed = embed )

@client.command(name = "work")
@commands.cooldown(1, 60, commands.BucketType.user)
async def work(ctx: commands.Context) -> None:
    database.money_wallet(ctx.author.id, 25)
    
    embed = discord.Embed( color = 0xff0000, title = f"nice work! \nyou earned 25 coins" )
    
    await ctx.send( embed = embed )

@client.command(name = "deposit", aliases = ["dep"])
async def deposit(ctx: commands.Context, amount: str = None) -> None:
    """
        from wallet to bank
    """
    if amount == None:
        embed = discord.Embed( color = 0xff0000, title = "how much are you withdrawing dumbass?" )
        await ctx.send( embed = embed )
        return

    
    if amount.lower() == "all" or amount.lower() == "max":
        amount = database[ctx.author.id]["wallet"]
    elif int(amount) <= 0:
        embed = discord.Embed( color = 0xff0000, title = "you're a real dumbass, aren't you?" )
        await ctx.send( embed = embed )
        return
    else:
        amount = int(amount)
    
    if database.deposit(ctx.author.id, amount):
        embed = discord.Embed( color = 0xff0000, title = f"success!\nyou successfully deposited {amount}" )
        await ctx.send( embed = embed )
    else:
        embed = discord.Embed( color = 0xff0000, title = "you don't have enough funds stupid" )
        await ctx.send( embed = embed )

@client.command(name = "withdraw")
async def withdraw(ctx: commands.Context, amount: str = None) -> None:
    """
        from bank to wallet
    """
    if amount == None:
        embed = discord.Embed( color = 0xff0000, title = "how much are you withdrawing dumbass?" )
        await ctx.send( embed = embed )
        return

    if amount.lower() == "all" or amount.lower() == "max":
        amount = database[ctx.author.id]["bank"]
    elif int(amount) <= 0:
        embed = discord.Embed( color = 0xff0000, title = "you're a real dumbass, aren't you?" )
        await ctx.send( embed = embed )
        return
    else:
        amount = int(amount)
    
    if database.withdraw(ctx.author.id, amount):
        embed = discord.Embed( color = 0xff0000, title = f"success!\nyou successfully deposited {amount}" )
        await ctx.send( embed = embed )
    else:
        embed = discord.Embed( color = 0xff0000, title = "you don't have enough funds stupid" )
        await ctx.send( embed = embed )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    # load_extensions() ditch cogs
    client.run(TOKEN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    except Exception as e:
        print(e)
    finally:
        database.close()
        database.generate_csv()
