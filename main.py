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


def load_extensions():
    for i in os.listdir("cogs"):
        client.load_extension(f"cogs.{i[:-3]}")
        print(f"{i:[-3]} loaded.")


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
