# built-ins
import os
import random

# 3rd party libraries
import discord
from discord.ext import commands
from discord.ext import tasks

# local imports
from utils import *
from supersecrets import TOKEN
from database import database

# ~~~~~~~~~~~~~~~~~~~~~~~

# globals
PREFIX = "."
client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
client.remove_command("help")
# ~~~~~~~~~~~~~~~~~~~~~~~

@tasks.loop(seconds = 120)
async def save_database() -> None:
    database._save()
    database.generate_csv()

@client.event
async def on_ready():
    old_user_count = len(database)
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            if member.bot:
                continue
            if member.id not in database:
                database.add_user(member.id, member.name)
            else:
                tmp_user = database[member.id]
                if tmp_user["name"] != member.name:
                    old_name = tmp_user["name"]
                    tmp_user["name"] = member.name
                    database[member.id] = tmp_user
                    warn(f"{old_name}'s name updated to {tmp_user['name']}")

    warn(f"added {len(database) - old_user_count} new users")

    await client.change_presence(activity=discord.Game(F"{PREFIX}help"))
    ok("Bot is online")

@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(color=0xFF0000, title="unhandled error")
    embed.add_field(name="error:", value=error, inline=False)
    await ctx.send(embed=embed)
    warn(error)

@client.event
async def on_member_join(member):
    if member.bot:
        return
    if member.id not in database:
        database.add_user(member.id, member.name)

# utils
async def dm_user(_id: str, *, message: str = None, embed: discord.Embed = None) -> None:
    """
        dm an user by their id
    """
    user = client.get_user(_id)
    if message == None:
        await user.send(embed=embed)
    elif embed == None:
        await user.send(message)
    else:
        warn("what are you sending this user?")

@client.command(name = "help")
async def help_command(ctx, _type: str = None):
    em = discord.Embed(title="Categories", color=0xFF0000)
    em.set_footer(
        text="type `.help [category] for help with a specific category or command`"
    )
    if not _type:
        em.set_author(name="Help")
        categories = "**Currency**\n**Information**"
        em.description = categories
    elif _type.lower() == "currency":
        em.title = "Currency Commands"
        currency_commands = [
            "**Balance**",
            "**Rob**",
            "**Work**",
            "**Deposit**",
            "**Withdraw**",
            "**Give**",
        ]
        currency_commands = ", ".join(currency_commands)
        em.description = currency_commands
    await ctx.send(embed=em)

@client.command(name = "info")
async def info(ctx: commands.Context, user: discord.Member = None):
    if not user: 
        user = ctx.author

    embed: discord.Embed = discord.Embed( 
        title = f"{user.name}#{user.discriminator}'s info", 
        color = 0xff0000
        )
    embed.add_field( 
        name   = "creation time",
        value  = str(user.created_at),
        inline = False
        )
    embed.add_field( 
        name   = "id",
        value  = user.id,
        inline = False
        )
    embed.add_field( 
        name   = "is bot?",
        value  = user.bot,
        inline = False
        )
    embed.set_image(
        url = user.avatar_url
    )

    await ctx.send(embed=embed)

#TODO add query commands for mods

@client.command(name = "rank", aliases = ["leaderboard"])
async def _rank(ctx: commands.Context) -> None:
    users = []
    async for user in ctx.guild.fetch_members( limit = None ):
        if not user.bot:
            users.append(database[user.id])

    sorted_users = sorted(users, key = lambda x: x["amount"], reverse = True)[0:10]

    embed = discord.Embed(
        title = f"{ctx.guild.name} leaderboard",
        color = 0xff0000,
    )
    for user_index in range(len(sorted_users)):
        embed.add_field(
            name   = f"#{user_index + 1} {sorted_users[user_index]['name']}",
            value  = str(sorted_users[user_index]["amount"]) + " ⏣",
            inline = False 
        )
    await ctx.send( embed = embed)

@client.command(name = "bal", aliases = ["balanace"])
async def balance(ctx: commands.Context, user: discord.Member = None) -> None:
    if not user: user = ctx.author
    _id = user.id
    
    embed = discord.Embed( 
        color = 0xff0000, 
        title = f"{database[_id]['name']}'s balance" 
        )
    embed.add_field(
        name = "total amount",
        value = f"{database[_id]['amount']} ⏣",
        inline = False 
        )
    await ctx.send( embed = embed )

@client.command(name = "work")
@commands.cooldown(1, 30, commands.BucketType.user)
async def work(ctx: commands.Context) -> None:
    database.work(ctx.author.id)
    embed = discord.Embed( 
        color = 0xff0000, 
        title = f"nice work! \nyou earned 25 ⏣"
        )
    await ctx.send( embed = embed )

@client.command(name = "give")
async def give(ctx: commands.Context, user: discord.Member, amount: str) -> None:
    _id = user.id
    if amount.lower() == "all" or amount.lower() == "max":
        amount = database[ctx.author.id]["amount"]
    else:
        if int(amount) > 0:
            amount = int(amount)
        else:
            embed = discord.Embed( 
                color = 0xff0000, 
                title = f"what are you trying to do here 🤨⁉"
            )
            await ctx.send(embed = embed)
            return

    if database.give(ctx.author.id, _id, amount):
        embed = discord.Embed( 
            color = 0xff0000, 
            title = f"you successfully gave {database[_id]['name']} {amount} ⏣"
            )
        # embed2 = discord.Embed(
        #     color = 0xff0000, 
        #     title = f"{database[ctx.author.id]['name']} gave you {amount} coins"
        #     )
        # await dm_user(_id, embed = embed2)
    else:
        embed = discord.Embed( 
            color = 0xff0000, 
            title = f"you don't have enough money dumbass"
            )

    await ctx.send( embed = embed )

def main():
    save_database.start()
    client.run(TOKEN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(e)
    finally:
        database.close()
        database.generate_csv()