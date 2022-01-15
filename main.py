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
# utils
async def dm_user(
    _id: str, *, message: str = None, embed: discord.Embed = None
) -> None:
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


# TODO add query commands for mods


@tasks.loop(seconds=120)
async def save_database() -> None:
    database._save()
    database.generate_csv()

<<<<<<< HEAD
=======
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


def load_extensions() -> None:
    for file_name in os.listdir("./cogs"):
        if file_name.endswith(".py"):
            client.load_extension(f"cogs.{file_name[:-3]}")
>>>>>>> 0b4433ea0beb6198635a259c59be53d902266809

def main():
    load_extensions()
    save_database.start()
    client.run(TOKEN)


if __name__ == "__main__":
    try:
        for cog in os.listdir("cogs"):
            client.load_extension(f"cogs.{cog[:-3]}")
            print(f"{cog[:-3]} Loaded.")
        main()

    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(e)
    finally:
        database.close()
        database.generate_csv()
